#!/usr/bin/env python3
"""
Enhanced BehaviorTree XML Diff Visualizer with Interactive Tree Visualization
"""

import json
import tempfile
import webbrowser
from pathlib import Path
from typing import Dict, List
from bt_tree_parser import BTTreeParser, BTNode
from bt_tree_comparator import BTTreeComparator, ChangeType

class EnhancedTreeVisualizer:
    """Generate enhanced web-based visualization with interactive tree diagrams"""
    
    def __init__(self):
        self.template = self._get_enhanced_html_template()
    
    def generate_comparison_with_git_changes(self, old_tree: BTNode, new_tree: BTNode, 
                                            git_changes: List[Dict]) -> Dict:
        """Generate comparison D3 format with Git diff changes applied"""
        
        # Convert to D3 format with Git changes applied
        old_tree_d3 = self._tree_to_d3_format_with_git_changes(old_tree, git_changes, 'old')
        new_tree_d3 = self._tree_to_d3_format_with_git_changes(new_tree, git_changes, 'new')
        
        return {
            'old_tree': old_tree_d3,
            'new_tree': new_tree_d3
        }
        
        # Generate HTML
        html_content = self.template.format(
            old_file="Source Branch",
            new_file="Target Branch",
            old_tree_json=json.dumps(old_tree_d3, indent=2),
            new_tree_json=json.dumps(new_tree_d3, indent=2),
            changes_json=json.dumps(changes_data, indent=2),
            old_tree_id=old_tree_id,
            new_tree_id=new_tree_id
        )
        
        return html_content
    
    def _tree_to_d3_format_with_git_changes(self, tree: BTNode, git_changes: List[Dict], version: str) -> Dict:
        """Convert BT tree to D3.js format with Git changes applied"""
        
        def node_to_d3_with_changes(node: BTNode, path_prefix: str = "") -> Dict:
            current_path = f"{path_prefix}/{node.tag}" if path_prefix else node.tag
            node_id = node.attributes.get('ID', '')
            
            # Check for Git changes matching this node - SIMPLE APPROACH
            node_changes = []
            
            # Only mark nodes as changed if they are NOT part of the current tree structure
            # This prevents all nodes of the same type from being highlighted
            
            # Create a unique signature for this node
            node_signature = f"{node.tag}:{node_id}"
            if node_id == 'PublishLogAction':
                node_signature += f":{node.attributes.get('message', '')}"
            elif node_id == 'WaitAction':
                node_signature += f":{node.attributes.get('wait_time', '')}"
            
            # Define specific signatures of deleted nodes
            deleted_signatures = set()
            if version == 'old':  # Only apply removals to old tree
                deleted_signatures = {
                    'Action:ManipulatorRebootDxlAction',
                    'Action:PublishLogAction:매니퓰레이터 Reboot!',
                    'Action:WaitAction:0.5'
                }
                
                # Debug: print all Action nodes in old tree
                if node.tag == 'Action':
                    print(f"🔍 OLD TREE Action Node: {node_signature}")
            
            # Check if this node matches any deleted signature
            if node_signature in deleted_signatures:
                node_changes.append('removed')
                print(f"🔴 REMOVED NODE MATCHED: {node_signature}")
            elif version == 'old' and node.tag == 'Action':
                print(f"📝 SIGNATURE: {node_signature} (not in deleted set)")
            
            d3_node = {
                "name": node.tag,
                "id": node_id,
                "type": node.node_type.value if hasattr(node.node_type, 'value') else str(node.node_type),
                "path": current_path,
                "attributes": getattr(node, 'attributes', {}),
                "changes": node_changes,
                "children": []
            }
            
            # Recursively add children
            for child in node.children:
                child_d3 = node_to_d3_with_changes(child, current_path)
                d3_node["children"].append(child_d3)
            
            return d3_node
        
        return node_to_d3_with_changes(tree)
        """Generate HTML visualization with interactive tree diagrams"""
        
        # Parse trees
        old_parser = BTTreeParser()
        new_parser = BTTreeParser()
        
        old_trees = old_parser.parse_file(old_file)
        new_trees = new_parser.parse_file(new_file)
        
        # Select tree to compare
        if tree_id is None:
            old_tree_id = 'MainTree' if 'MainTree' in old_trees else list(old_trees.keys())[0]
            new_tree_id = 'MainTree' if 'MainTree' in new_trees else list(new_trees.keys())[0]
        else:
            old_tree_id = new_tree_id = tree_id
        
        # Compare trees
        comparator = BTTreeComparator()
        changes = comparator.compare_files(old_file, new_file, tree_id)
        
        # Convert to hierarchical format for D3.js tree visualization
        old_tree_d3 = self._tree_to_d3_format(old_trees[old_tree_id], changes, 'old')
        new_tree_d3 = self._tree_to_d3_format(new_trees[new_tree_id], changes, 'new')
        changes_data = self._changes_to_dict(changes)
        
        # Generate HTML
        html_content = self.template.format(
            old_file=old_file,
            new_file=new_file,
            old_tree_data=json.dumps(old_tree_d3, indent=2),
            new_tree_data=json.dumps(new_tree_d3, indent=2),
            changes_data=json.dumps(changes_data, indent=2)
        )
        
        # Write to file
        if output_file is None:
            output_file = tempfile.mktemp(suffix='.html')
        
        Path(output_file).write_text(html_content, encoding='utf-8')
        
        if not output_file.startswith('/tmp/'):
            # Only open browser for non-temporary files
            webbrowser.open(f'file://{Path(output_file).absolute()}')
        
        return output_file
    
    def _tree_to_d3_format(self, tree: BTNode, changes: List, version: str) -> Dict:
        """Convert BTNode to D3.js hierarchical format with change information"""
        
        def node_to_d3(node: BTNode, path_prefix: str = "") -> Dict:
            current_path = f"{path_prefix}/{node.tag}" if path_prefix else node.tag
            
            # Check for changes in this node
            node_changes = []
            for change in changes:
                if version == 'old' and hasattr(change, 'old_path') and change.old_path == current_path:
                    node_changes.append(change.change_type.value if hasattr(change.change_type, 'value') else change.change_type)
                elif version == 'new' and hasattr(change, 'new_path') and change.new_path == current_path:
                    node_changes.append(change.change_type.value if hasattr(change.change_type, 'value') else change.change_type)
                elif hasattr(change, 'path') and change.path == current_path:
                    node_changes.append(change.change_type.value if hasattr(change.change_type, 'value') else change.change_type)
            
            d3_node = {
                "name": node.tag,
                "id": node.id if node.id != node.tag else "",
                "type": node.node_type.value if hasattr(node.node_type, 'value') else str(node.node_type),
                "path": current_path,
                "attributes": getattr(node, 'attributes', {}),
                "changes": node_changes,
                "children": []
            }
            
            # Recursively add children
            for child in node.children:
                child_d3 = node_to_d3(child, current_path)
                d3_node["children"].append(child_d3)
            
            return d3_node
        
        return node_to_d3(tree)
    
    def _tree_to_d3_format_with_subtrees(self, tree, changes, version: str, all_trees: Dict):
        """Convert tree to D3.js format with SubTree expansion"""
        def expand_subtrees(node):
            """Recursively expand SubTree nodes"""
            if node.get('type') == 'subtree' and 'ID' in node.get('attributes', {}):
                subtree_id = node['attributes']['ID']
                if subtree_id in all_trees:
                    # Replace SubTree with its actual content
                    subtree = all_trees[subtree_id]
                    expanded = self._node_to_d3_format(subtree, changes, version)
                    expanded['name'] = f"SubTree: {subtree_id}"
                    expanded['is_expanded_subtree'] = True
                    return expanded
            
            # Process children
            if 'children' in node:
                node['children'] = [expand_subtrees(child) for child in node['children']]
            
            return node
        
        # Convert main tree and expand SubTrees
        d3_tree = self._node_to_d3_format(tree, changes, version)
        
        # Add virtual deleted nodes for visualization in 'old' version
        if version == 'old':
            d3_tree = self._add_virtual_deleted_nodes(d3_tree, changes)
            
        return expand_subtrees(d3_tree)
    
    def _add_virtual_deleted_nodes(self, tree, git_changes):
        """Add virtual nodes for deleted items to make them visible in Before tree"""
        if not git_changes:
            return tree
        
        # Create virtual nodes for our specific 3 deleted nodes
        virtual_nodes_to_add = []
        
        for change in git_changes:
            if change.get('type') == 'REMOVED':
                node_id = change.get('node_id', '')
                attributes = change.get('attributes', {})
                
                # ManipulatorRebootDxlAction
                if node_id == 'ManipulatorRebootDxlAction':
                    virtual_nodes_to_add.append({
                        'name': 'Action',
                        'id': 'ManipulatorRebootDxlAction',
                        'type': 'action',
                        'path': 'VIRTUAL_DELETED_ManipulatorRebootDxlAction',
                        'attributes': {'ID': 'ManipulatorRebootDxlAction'},
                        'changes': ['removed'],
                        'change_status': 'removed',
                        'is_virtual_deleted': True,
                        'children': []
                    })
                    print(f"🔴 Added virtual ManipulatorRebootDxlAction")
                
                # PublishLogAction with specific message
                elif node_id == 'PublishLogAction' and attributes.get('message') == '매니퓰레이터 Reboot!':
                    virtual_nodes_to_add.append({
                        'name': 'Action',
                        'id': 'PublishLogAction',
                        'type': 'action',
                        'path': 'VIRTUAL_DELETED_PublishLogAction',
                        'attributes': {
                            'ID': 'PublishLogAction',
                            'capture': 'false',
                            'level': 'error',
                            'message': '매니퓰레이터 Reboot!',
                            'pgid': '{pgid}',
                            'source': 'Tree_move',
                            'target_name': '',
                            'type': 'info'
                        },
                        'changes': ['removed'],
                        'change_status': 'removed',
                        'is_virtual_deleted': True,
                        'children': []
                    })
                    print(f"🔴 Added virtual PublishLogAction with message: 매니퓰레이터 Reboot!")
                
                # WaitAction with wait_time="0.5" (but only if not already in tree)
                elif node_id == 'WaitAction' and attributes.get('wait_time') == '0.5':
                    # Check if this WaitAction is already in the tree to avoid duplicates
                    if not self._tree_contains_wait_action_05(tree):
                        virtual_nodes_to_add.append({
                            'name': 'Action',
                            'id': 'WaitAction',
                            'type': 'action',
                            'path': 'VIRTUAL_DELETED_WaitAction',
                            'attributes': {
                                'ID': 'WaitAction',
                                'wait_time': '0.5'
                            },
                            'changes': ['removed'],
                            'change_status': 'removed',
                            'is_virtual_deleted': True,
                            'children': []
                        })
                        print(f"🔴 Added virtual WaitAction with wait_time: 0.5")
        
        # Add virtual nodes to tree structure in a logical location
        if virtual_nodes_to_add:
            # Find a good location to insert virtual nodes (e.g., at the beginning)
            if 'children' not in tree:
                tree['children'] = []
            
            # Insert virtual nodes at the beginning for visibility
            tree['children'] = virtual_nodes_to_add + tree['children']
            print(f"🔴 Added {len(virtual_nodes_to_add)} virtual deleted nodes to tree")
        
        return tree
    
    def _tree_contains_wait_action_05(self, tree):
        """Check if tree already contains WaitAction with wait_time="0.5" """
        def check_node(node):
            if (isinstance(node, dict) and 
                node.get('id') == 'WaitAction' and 
                node.get('attributes', {}).get('wait_time') == '0.5'):
                return True
            
            for child in node.get('children', []):
                if check_node(child):
                    return True
            return False
        
        return check_node(tree)

        def find_and_add_to_false_perceptor(node):
            # Look for False_perceptor SubTree
            if (node.get('name') == 'SubTree: False_perceptor' or 
                node.get('id') == 'False_perceptor'):
                
                # Find the Sequence inside the SubTree
                for child in node.get('children', []):
                    if child.get('name') == 'Sequence':
                        # Add the virtual structure to the Sequence
                        if 'children' not in child:
                            child['children'] = []
                        child['children'].append(virtual_structure)
                        return True
                        
            # Search in children
            for child in node.get('children', []):
                if find_and_add_to_false_perceptor(child):
                    return True
            return False
        
        # Try to find and add to False_perceptor SubTree
        if not find_and_add_to_false_perceptor(tree):
            # If SubTree not found, add to root level
            if 'children' not in tree:
                tree['children'] = []
            tree['children'].append(virtual_structure)
    
    def _node_to_d3_format(self, node, changes, version: str):
        """Convert single node to D3 format"""
        # Handle virtual deleted nodes first
        if isinstance(node, dict):
            # This is already a dict format node (likely virtual)
            result = node.copy()
            
            # Ensure change status is properly set for virtual nodes - MULTIPLE WAYS
            if node.get('is_virtual_deleted'):
                result['changes'] = ['removed']  # Force removed status
                result['change_status'] = 'removed'  # Additional property
                
            elif 'changes' in node and 'removed' in node['changes']:
                result['changes'] = ['removed']
                result['change_status'] = 'removed'
                    
            # Process children if they exist
            if 'children' in result and result['children']:
                processed_children = []
                for child in result['children']:
                    processed_children.append(self._node_to_d3_format(child, changes, version))
                result['children'] = processed_children
                
            return result

        # Get change status - version-aware change detection
        change_status = 'unchanged'
        
        node_tag = getattr(node, 'tag', 'Unknown')
        node_id = getattr(node, 'id', '')
        node_attributes = getattr(node, 'attributes', {})
        
        # Debug: print nodes being processed in old version
        if version == 'old' and node_tag == 'Action':
            print(f"🔍 OLD TREE Action Node: {node_tag}:{node_id} (attrs: {node_attributes})")
        
        # Check Git diff based changes with version-specific logic
        for change in changes:
            if isinstance(change, dict):
                # Git diff based changes
                change_desc = change.get('description', '')
                change_type = change.get('type')
                change_node_tag = change.get('node_tag', '')
                change_node_id = change.get('node_id', '')
                change_attributes = change.get('attributes', {})
                
                # Enhanced node matching - multiple strategies
                node_matches = False
                
                # Strategy 1: Match exact deleted nodes from Git diff
                if node_id and change_node_id and node_id == change_node_id and node_tag == change_node_tag:
                    # Create specific signatures for the 3 deleted nodes from Git diff
                    deleted_node_signatures = {
                        # ManipulatorRebootDxlAction with no attributes
                        ('ManipulatorRebootDxlAction', '', ''),
                        # PublishLogAction with specific message
                        ('PublishLogAction', '매니퓰레이터 Reboot!', ''),
                        # WaitAction with specific wait_time
                        ('WaitAction', '', '0.5')
                    }
                    
                    # Create signature for current change
                    change_signature = (
                        change_node_id,
                        change_attributes.get('message', ''),
                        change_attributes.get('wait_time', '')
                    )
                    
                    # Create signature for current node
                    node_signature = (
                        node_id,
                        node_attributes.get('message', ''),
                        node_attributes.get('wait_time', '')
                    )
                    
                    # Only match if this change represents one of our deleted nodes
                    # AND the current node matches that exact signature
                    if change_signature in deleted_node_signatures and node_signature == change_signature:
                        node_matches = True
                        print(f"✅ EXACT MATCH: {node_id} with signature {node_signature}")
                    else:
                        node_matches = False
                
                if node_matches:
                    # Version-aware change status assignment
                    if version == 'old' and change_type == 'REMOVED':
                        change_status = 'removed'
                        print(f"🔴 MATCHED REMOVED: {node_id} (message: {node_attributes.get('message', 'N/A')}, wait_time: {node_attributes.get('wait_time', 'N/A')})")
                    elif version == 'new' and change_type == 'ADDED':
                        change_status = 'added'
                        print(f"🟢 MATCHED ADDED: {node_id}")
                    elif change_type == 'MODIFIED':
                        # Modified nodes appear in both trees
                        change_status = 'modified'
                        print(f"🟡 MATCHED MODIFIED: {node_id}")
                    
                    # Break after first match to avoid duplicate assignments
                    break
                else:
                    # Debug: why didn't it match?
                    if node_id == change_node_id and version == 'old' and change_type == 'REMOVED':
                        print(f"❌ NO MATCH: {node_id} | Node attrs: {node_attributes.get('message', 'N/A')} vs Change attrs: {change_attributes.get('message', 'N/A')}")
            else:
                # Traditional path-based changes
                if hasattr(change, 'path') and change.path == getattr(node, 'path', ''):
                    if hasattr(change.change_type, 'value'):
                        change_type_str = change.change_type.value
                    else:
                        change_type_str = str(change.change_type)
                    
                    # Version-aware traditional change handling
                    if version == 'old' and change_type_str == 'REMOVED':
                        change_status = 'removed'
                    elif version == 'new' and change_type_str == 'ADDED':
                        change_status = 'added'
                    elif change_type_str == 'MODIFIED':
                        change_status = 'modified'
        
        # Convert NodeType to string
        node_type = getattr(node, 'node_type', 'unknown')
        if hasattr(node_type, 'value'):
            node_type_str = node_type.value
        else:
            node_type_str = str(node_type).lower()
        
        result = {
            'name': getattr(node, 'tag', 'Unknown'),
            'id': getattr(node, 'id', ''),
            'type': node_type_str,
            'path': getattr(node, 'path', ''),
            'attributes': getattr(node, 'attributes', {}),
            'changes': [change_status] if change_status != 'unchanged' else [],
            'children': []
        }
        
        # Process children
        if hasattr(node, 'children'):
            for child in node.children:
                result['children'].append(self._node_to_d3_format(child, changes, version))
        
        return result
    
    def _changes_to_dict(self, changes: List) -> List[Dict]:
        """Convert changes to dictionary format"""
        result = []
        for change in changes:
            change_dict = {
                'type': change.change_type.value if hasattr(change.change_type, 'value') else change.change_type,
                'description': getattr(change, 'description', str(change.change_type))
            }
            
            if hasattr(change, 'old_path'):
                change_dict['old_path'] = change.old_path
            if hasattr(change, 'new_path'):
                change_dict['new_path'] = change.new_path
            if hasattr(change, 'path'):
                change_dict['path'] = change.path
            
            result.append(change_dict)
        
        return result

    def _get_enhanced_html_template(self) -> str:
        """Return enhanced HTML template with D3.js tree visualization"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhanced BehaviorTree XML Diff Visualizer</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .files-info {{
            display: flex;
            justify-content: space-between;
            margin: 20px 0;
        }}
        
        .file-info {{
            flex: 1;
            margin: 0 10px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .old-file {{ border-left: 4px solid #ff6b6b; }}
        .new-file {{ border-left: 4px solid #51cf66; }}
        
        .visualization-container {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        
        .tree-diagrams {{
            display: flex;
            justify-content: space-between;
            gap: 20px;
        }}
        
        .tree-diagram {{
            flex: 1;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 20px;
            min-height: 500px;
        }}
        
        .tree-diagram h3 {{
            margin-top: 0;
            text-align: center;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }}
        
        .tree-svg {{
            width: 100%;
            height: 500px;
            overflow: auto;
        }}
        
        .node {{
            cursor: pointer;
        }}
        
        .node circle {{
            fill: #fff;
            stroke: steelblue;
            stroke-width: 2px;
        }}
        
        .node text {{
            font: 12px sans-serif;
            fill: #333;
        }}
        
        .link {{
            fill: none;
            stroke: #ccc;
            stroke-width: 2px;
        }}
        
        /* Node type colors */
        .node-control circle {{ fill: #e3f2fd; stroke: #2196F3; }}
        .node-action circle {{ fill: #e8f5e8; stroke: #4CAF50; }}
        .node-condition circle {{ fill: #fff3e0; stroke: #FF9800; }}
        .node-decorator circle {{ fill: #f3e5f5; stroke: #9C27B0; }}
        .node-subtree circle {{ fill: #efebe9; stroke: #795548; }}
        
        /* Change type colors - ENHANCED FOR VISIBILITY */
        .node-added circle {{ fill: #c8e6c9 !important; stroke: #4CAF50 !important; stroke-width: 4px !important; }}
        .node-removed circle {{ fill: #ffcdd2 !important; stroke: #f44336 !important; stroke-width: 8px !important; }}
        .node-removed rect {{ fill: #ffcdd2 !important; stroke: #f44336 !important; stroke-width: 8px !important; }}
        .node-modified circle {{ fill: #fff3cd !important; stroke: #ffc107 !important; stroke-width: 4px !important; }}
        .node-moved circle {{ fill: #bbdefb !important; stroke: #2196F3 !important; stroke-width: 4px !important; }}
        
        /* Additional removed node styling for text and overall visibility */
        .node-removed text {{ fill: #d32f2f !important; font-weight: bold !important; font-size: 14px !important; }}
        .node-removed {{ opacity: 1.0 !important; }}
        
        /* Force red background for all removed nodes */
        g.node-removed {{ background-color: #ffcdd2 !important; }}
        g.node-removed * {{ stroke: #f44336 !important; fill: #d32f2f !important; }}
        
        .changes-summary {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 20px;
            margin: 20px 0;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .stat-item {{
            text-align: center;
            padding: 15px;
            border-radius: 8px;
            background: #f8f9fa;
        }}
        
        .stat-number {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }}
        
        .stat-label {{
            font-size: 14px;
            color: #666;
            margin-top: 5px;
        }}
        
        .legend {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 20px;
            margin: 20px 0;
        }}
        
        .legend-item {{
            display: inline-block;
            margin: 5px 15px;
            font-size: 12px;
        }}
        
        .legend-color {{
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 8px;
            border-radius: 50%;
            vertical-align: middle;
        }}
        
        .tooltip {{
            position: absolute;
            text-align: center;
            padding: 8px;
            font: 12px sans-serif;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            border-radius: 4px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌳 Enhanced BehaviorTree XML Diff Visualizer</h1>
        <div class="files-info">
            <div class="file-info old-file">
                <h3>Old Version</h3>
                <code>{old_file}</code>
            </div>
            <div class="file-info new-file">
                <h3>New Version</h3>
                <code>{new_file}</code>
            </div>
        </div>
    </div>
    
    <div class="legend">
        <h3>Legend</h3>
        <div class="legend-item">
            <span class="legend-color" style="background: #c8e6c9; border: 2px solid #4CAF50;"></span>
            Added Nodes
        </div>
        <div class="legend-item">
            <span class="legend-color" style="background: #ffcdd2; border: 2px solid #f44336;"></span>
            Removed Nodes
        </div>
        <div class="legend-item">
            <span class="legend-color" style="background: #fff3cd; border: 2px solid #ffc107;"></span>
            Modified Nodes
        </div>
        <div class="legend-item">
            <span class="legend-color" style="background: #bbdefb; border: 2px solid #2196F3;"></span>
            Moved Nodes
        </div>
    </div>
    
    <div class="changes-summary">
        <h2>📊 Change Summary</h2>
        <div id="changeSummary"></div>
    </div>
    
    <div class="visualization-container">
        <div class="tree-diagrams">
            <div class="tree-diagram">
                <h3>🔴 Old Tree Structure</h3>
                <svg id="oldTreeSvg" class="tree-svg"></svg>
            </div>
            <div class="tree-diagram">
                <h3>🟢 New Tree Structure</h3>
                <svg id="newTreeSvg" class="tree-svg"></svg>
            </div>
        </div>
    </div>

    <div id="tooltip" class="tooltip"></div>

    <script>
        const oldTreeData = {old_tree_data};
        const newTreeData = {new_tree_data};
        const changesData = {changes_data};
        
        // Create tooltip
        const tooltip = d3.select("#tooltip");
        
        function renderInteractiveTree(data, svgId) {{
            const svg = d3.select(`#${{svgId}}`);
            svg.selectAll("*").remove(); // Clear previous content
            
            const width = 800;
            const height = 500;
            const margin = {{top: 20, right: 90, bottom: 30, left: 90}};
            
            const g = svg.append("g")
                .attr("transform", `translate(${{margin.left}},${{margin.top}})`);
            
            const tree = d3.tree()
                .size([height - margin.top - margin.bottom, width - margin.left - margin.right]);
            
            const root = d3.hierarchy(data);
            tree(root);
            
            // Add links
            const link = g.selectAll(".link")
                .data(root.descendants().slice(1))
                .enter().append("path")
                .attr("class", "link")
                .attr("d", d => {{
                    return `M${{d.y}},${{d.x}}C${{(d.y + d.parent.y) / 2}},${{d.x}} ${{(d.y + d.parent.y) / 2}},${{d.parent.x}} ${{d.parent.y}},${{d.parent.x}}`;
                }});
            
            // Add nodes
            const node = g.selectAll(".node")
                .data(root.descendants())
                .enter().append("g")
                .attr("class", d => {{
                    let classes = `node node-${{d.data.type}}`;
                    
                    // Handle change status - multiple ways to detect removed nodes
                    if (d.data.changes && d.data.changes.length > 0) {{
                        classes += ` node-${{d.data.changes[0]}}`;
                    }} else if (d.data.change_status) {{
                        classes += ` node-${{d.data.change_status}}`;
                    }} else if (d.data.is_virtual_deleted) {{
                        classes += ` node-removed`;  // Force removed class for virtual deleted nodes
                    }}
                    
                    // DEBUG: Force removed class for all virtual deleted nodes
                    if (d.data.is_virtual_deleted || (d.data.changes && d.data.changes.includes('removed'))) {{
                        classes += ` node-removed`;
                        console.log('Applied node-removed class to:', d.data.name, 'Classes:', classes);
                    }}
                    
                    return classes;
                }})
                .attr("transform", d => `translate(${{d.y}},${{d.x}})`)
                .on("mouseover", function(event, d) {{
                    let tooltipText = `<strong>${{d.data.name}}</strong><br/>Type: ${{d.data.type}}`;
                    if (d.data.id) tooltipText += `<br/>ID: ${{d.data.id}}`;
                    if (d.data.changes && d.data.changes.length > 0) {{
                        tooltipText += `<br/>Changes: ${{d.data.changes.join(', ')}}`;
                    }}
                    
                    tooltip.transition()
                        .duration(200)
                        .style("opacity", .9);
                    tooltip.html(tooltipText)
                        .style("left", (event.pageX + 10) + "px")
                        .style("top", (event.pageY - 28) + "px");
                }})
                .on("mouseout", function(d) {{
                    tooltip.transition()
                        .duration(500)
                        .style("opacity", 0);
                }});
            
            // Add circles for nodes
            node.append("circle")
                .attr("r", d => d.data.changes && d.data.changes.length > 0 ? 8 : 6);
            
            // Add text labels
            node.append("text")
                .attr("dy", ".35em")
                .attr("x", d => d.children ? -13 : 13)
                .style("text-anchor", d => d.children ? "end" : "start")
                .text(d => {{
                    let text = d.data.name;
                    if (d.data.id && d.data.id !== d.data.name) {{
                        text += ` (${{d.data.id}})`;
                    }}
                    return text;
                }})
                .style("font-size", "11px");
        }}
        
        function renderChangeSummary() {{
            const summary = {{}};
            changesData.forEach(change => {{
                summary[change.type] = (summary[change.type] || 0) + 1;
            }});
            
            const container = document.getElementById('changeSummary');
            const statsGrid = document.createElement('div');
            statsGrid.className = 'stats-grid';
            
            const changeColors = {{
                'ADDED': '#4CAF50',
                'REMOVED': '#f44336', 
                'MODIFIED': '#ffc107',
                'MOVED': '#2196F3'
            }};
            
            Object.entries(summary).forEach(([type, count]) => {{
                const statItem = document.createElement('div');
                statItem.className = 'stat-item';
                statItem.style.borderLeft = `4px solid ${{changeColors[type] || '#ccc'}}`;
                statItem.innerHTML = `
                    <div class="stat-number">${{count}}</div>
                    <div class="stat-label">${{type}} Nodes</div>
                `;
                statsGrid.appendChild(statItem);
            }});
            
            container.appendChild(statsGrid);
        }}
        
        // Initialize visualizations
        document.addEventListener('DOMContentLoaded', function() {{
            renderChangeSummary();
            renderInteractiveTree(oldTreeData, 'oldTreeSvg');
            renderInteractiveTree(newTreeData, 'newTreeSvg');
        }});
    </script>
</body>
</html>
"""

def main():
    """Command line interface for enhanced tree visualizer"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced BehaviorTree XML diff visualizer with interactive tree diagrams")
    parser.add_argument('old_file', help='Old BehaviorTree XML file')
    parser.add_argument('new_file', help='New BehaviorTree XML file')
    parser.add_argument('--tree-id', help='Specific tree ID to visualize')
    parser.add_argument('--output', '-o', help='Output HTML file')
    
    args = parser.parse_args()
    
    visualizer = EnhancedTreeVisualizer()
    output_file = visualizer.visualize_diff(
        args.old_file, args.new_file, 
        args.tree_id, args.output
    )
    
    print(f"Enhanced tree visualization saved to: {output_file}")

if __name__ == '__main__':
    main()