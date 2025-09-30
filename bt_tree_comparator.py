#!/usr/bin/env python3
"""
BehaviorTree XML Structure Comparator
"""

from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass
from enum import Enum
from bt_tree_parser import BTTreeParser, BTNode, NodeType
import difflib

class ChangeType(Enum):
    ADDED = "added"
    REMOVED = "removed"
    MOVED = "moved"
    MODIFIED = "modified"
    UNCHANGED = "unchanged"

@dataclass
class NodeChange:
    """Represents a change to a node"""
    change_type: ChangeType
    old_node: Optional[BTNode] = None
    new_node: Optional[BTNode] = None
    old_path: Optional[str] = None
    new_path: Optional[str] = None
    attribute_changes: Dict[str, Tuple[str, str]] = None
    
class BTTreeComparator:
    """Compare two BehaviorTree XML structures"""
    
    def __init__(self):
        self.changes: List[NodeChange] = []
        
    def compare_files(self, old_file: str, new_file: str, tree_id: str = None) -> List[NodeChange]:
        """Compare two BehaviorTree XML files"""
        
        # Parse both files
        old_parser = BTTreeParser()
        new_parser = BTTreeParser()
        
        old_trees = old_parser.parse_file(old_file)
        new_trees = new_parser.parse_file(new_file)
        
        # Select tree to compare
        if tree_id is None:
            # Compare the first tree found, or MainTree if available
            old_tree_id = 'MainTree' if 'MainTree' in old_trees else list(old_trees.keys())[0]
            new_tree_id = 'MainTree' if 'MainTree' in new_trees else list(new_trees.keys())[0]
        else:
            old_tree_id = new_tree_id = tree_id
            
        if old_tree_id not in old_trees:
            raise ValueError(f"Tree '{old_tree_id}' not found in old file")
        if new_tree_id not in new_trees:
            raise ValueError(f"Tree '{new_tree_id}' not found in new file")
            
        return self.compare_trees(old_trees[old_tree_id], new_trees[new_tree_id])
    
    def compare_trees(self, old_root: BTNode, new_root: BTNode) -> List[NodeChange]:
        """Compare two tree structures"""
        self.changes = []
        
        # Create node maps for efficient lookup
        old_nodes = self._create_node_map(old_root)
        new_nodes = self._create_node_map(new_root)
        
        # Find all unique paths
        all_paths = set(old_nodes.keys()) | set(new_nodes.keys())
        
        for path in all_paths:
            old_node = old_nodes.get(path)
            new_node = new_nodes.get(path)
            
            if old_node and new_node:
                # Node exists in both - check for modifications
                self._compare_nodes(old_node, new_node, path)
            elif old_node and not new_node:
                # Node removed
                self.changes.append(NodeChange(
                    change_type=ChangeType.REMOVED,
                    old_node=old_node,
                    old_path=path
                ))
            elif not old_node and new_node:
                # Node added
                self.changes.append(NodeChange(
                    change_type=ChangeType.ADDED,
                    new_node=new_node,
                    new_path=path
                ))
        
        # Detect moved nodes (same node signature but different path)
        self._detect_moved_nodes(old_nodes, new_nodes)
        
        return self.changes
    
    def _create_node_map(self, root: BTNode) -> Dict[str, BTNode]:
        """Create a map of path -> node for efficient lookup"""
        node_map = {}
        self._traverse_and_map(root, node_map)
        return node_map
    
    def _traverse_and_map(self, node: BTNode, node_map: Dict[str, BTNode]):
        """Recursively traverse tree and build path map"""
        node_map[node.path] = node
        for child in node.children:
            self._traverse_and_map(child, node_map)
    
    def _compare_nodes(self, old_node: BTNode, new_node: BTNode, path: str):
        """Compare two nodes at the same path"""
        changes = {}
        
        # Check if basic properties changed
        if old_node.tag != new_node.tag:
            changes['tag'] = (old_node.tag, new_node.tag)
        if old_node.node_type != new_node.node_type:
            changes['node_type'] = (old_node.node_type.value, new_node.node_type.value)
            
        # Check attribute changes
        attr_changes = {}
        all_attrs = set(old_node.attributes.keys()) | set(new_node.attributes.keys())
        
        for attr in all_attrs:
            old_val = old_node.attributes.get(attr, '')
            new_val = new_node.attributes.get(attr, '')
            if old_val != new_val:
                attr_changes[attr] = (old_val, new_val)
        
        # If there are any changes, record them
        if changes or attr_changes:
            self.changes.append(NodeChange(
                change_type=ChangeType.MODIFIED,
                old_node=old_node,
                new_node=new_node,
                old_path=path,
                new_path=path,
                attribute_changes=attr_changes
            ))
        else:
            # Node unchanged
            self.changes.append(NodeChange(
                change_type=ChangeType.UNCHANGED,
                old_node=old_node,
                new_node=new_node,
                old_path=path,
                new_path=path
            ))
    
    def _detect_moved_nodes(self, old_nodes: Dict[str, BTNode], new_nodes: Dict[str, BTNode]):
        """Detect nodes that were moved (same signature, different path)"""
        # Create signature maps
        old_signatures = {}
        new_signatures = {}
        
        for path, node in old_nodes.items():
            sig = self._node_signature(node)
            if sig not in old_signatures:
                old_signatures[sig] = []
            old_signatures[sig].append((path, node))
            
        for path, node in new_nodes.items():
            sig = self._node_signature(node)
            if sig not in new_signatures:
                new_signatures[sig] = []
            new_signatures[sig].append((path, node))
        
        # Find potential moves
        for sig in old_signatures:
            if sig in new_signatures:
                old_instances = old_signatures[sig]
                new_instances = new_signatures[sig]
                
                # Simple case: one-to-one mapping with different paths
                if len(old_instances) == 1 and len(new_instances) == 1:
                    old_path, old_node = old_instances[0]
                    new_path, new_node = new_instances[0]
                    
                    if old_path != new_path:
                        # Remove the REMOVED and ADDED entries for this move
                        self.changes = [c for c in self.changes 
                                      if not ((c.change_type == ChangeType.REMOVED and c.old_path == old_path) or
                                             (c.change_type == ChangeType.ADDED and c.new_path == new_path))]
                        
                        # Add MOVED entry
                        self.changes.append(NodeChange(
                            change_type=ChangeType.MOVED,
                            old_node=old_node,
                            new_node=new_node,
                            old_path=old_path,
                            new_path=new_path
                        ))
    
    def _node_signature(self, node: BTNode) -> str:
        """Create a unique signature for a node to detect moves"""
        # Use tag, type, and key attributes to create signature
        key_attrs = ['ID', 'name', 'sub_tree_name']
        attr_parts = []
        for attr in key_attrs:
            if attr in node.attributes:
                attr_parts.append(f"{attr}={node.attributes[attr]}")
        
        return f"{node.tag}({node.node_type.value}):{':'.join(attr_parts)}"
    
    def generate_diff_report(self, old_file: str, new_file: str) -> str:
        """Generate a human-readable diff report"""
        report = []
        report.append(f"BehaviorTree XML Structural Diff")
        report.append(f"================================")
        report.append(f"Old file: {old_file}")
        report.append(f"New file: {new_file}")
        report.append("")
        
        # Statistics
        added_count = sum(1 for c in self.changes if c.change_type == ChangeType.ADDED)
        removed_count = sum(1 for c in self.changes if c.change_type == ChangeType.REMOVED)
        modified_count = sum(1 for c in self.changes if c.change_type == ChangeType.MODIFIED)
        moved_count = sum(1 for c in self.changes if c.change_type == ChangeType.MOVED)
        unchanged_count = sum(1 for c in self.changes if c.change_type == ChangeType.UNCHANGED)
        
        report.append(f"Summary:")
        report.append(f"  Added: {added_count}")
        report.append(f"  Removed: {removed_count}")
        report.append(f"  Modified: {modified_count}")
        report.append(f"  Moved: {moved_count}")
        report.append(f"  Unchanged: {unchanged_count}")
        report.append("")
        
        # Detailed changes
        for change in self.changes:
            if change.change_type == ChangeType.UNCHANGED:
                continue
                
            report.append(self._format_change(change))
            report.append("")
        
        return "\n".join(report)
    
    def _format_change(self, change: NodeChange) -> str:
        """Format a single change for the report"""
        if change.change_type == ChangeType.ADDED:
            return f"+ ADDED: {change.new_path}\n  {self._format_node_info(change.new_node)}"
            
        elif change.change_type == ChangeType.REMOVED:
            return f"- REMOVED: {change.old_path}\n  {self._format_node_info(change.old_node)}"
            
        elif change.change_type == ChangeType.MOVED:
            return f"→ MOVED: {change.old_path} → {change.new_path}\n  {self._format_node_info(change.new_node)}"
            
        elif change.change_type == ChangeType.MODIFIED:
            result = f"* MODIFIED: {change.old_path}"
            if change.attribute_changes:
                result += "\n  Attribute changes:"
                for attr, (old_val, new_val) in change.attribute_changes.items():
                    result += f"\n    {attr}: '{old_val}' → '{new_val}'"
            return result
        
        return ""
    
    def _format_node_info(self, node: BTNode) -> str:
        """Format node information"""
        info = f"{node.tag} ({node.node_type.value})"
        if node.attributes:
            key_attrs = ['ID', 'name', 'sub_tree_name']
            attr_info = []
            for attr in key_attrs:
                if attr in node.attributes:
                    attr_info.append(f"{attr}='{node.attributes[attr]}'")
            if attr_info:
                info += f" [{', '.join(attr_info)}]"
        return info