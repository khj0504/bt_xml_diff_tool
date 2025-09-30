#!/usr/bin/env python3
"""
BehaviorTree XML Parser for structural analysis
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class NodeType(Enum):
    CONTROL = "control"
    ACTION = "action" 
    CONDITION = "condition"
    DECORATOR = "decorator"
    SUBTREE = "subtree"

@dataclass
class BTNode:
    """Represents a single node in the behavior tree"""
    id: str
    node_type: NodeType
    tag: str
    attributes: Dict[str, str]
    children: List['BTNode']
    parent: Optional['BTNode'] = None
    depth: int = 0
    path: str = ""

class BTTreeParser:
    """Parser for BehaviorTree.CPP XML files"""
    
    # Common control flow nodes in BehaviorTree.CPP
    CONTROL_NODES = {
        'Sequence', 'Selector', 'Fallback', 'Parallel', 'ReactiveSequence',
        'ReactiveFallback', 'IfThenElse', 'WhileDoElse', 'ForEach',
        'Switch', 'StatefulActionNode', 'Control', 'MultiRobotControl'
    }
    
    DECORATOR_NODES = {
        'Inverter', 'ForceSuccess', 'ForceFailure', 'Repeat', 'Retry',
        'Timeout', 'Delay', 'BlackboardPrecondition', 'KeepRunningUntilFailure',
        'Decorator', 'ReportFailure', 'RetryUntilSuccessful',
        'BlackboardPostCheckString', 'BlackboardPostCheckInt', 'BlackboardPostCheckBool'
    }
    
    def __init__(self):
        self.trees: Dict[str, BTNode] = {}
        self.all_nodes: List[BTNode] = []
        
    def parse_file(self, file_path: str) -> Dict[str, BTNode]:
        """Parse a BehaviorTree XML file and return tree structures"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Find all BehaviorTree definitions
            for bt_element in root.findall('.//BehaviorTree'):
                tree_id = bt_element.get('ID', 'MainTree')
                bt_root = self._parse_element(bt_element, None, 0)
                bt_root.id = tree_id
                self.trees[tree_id] = bt_root
                
            return self.trees
            
        except ET.ParseError as e:
            raise ValueError(f"XML parsing error: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
    
    def _parse_element(self, element: ET.Element, parent: Optional[BTNode], depth: int) -> BTNode:
        """Recursively parse XML elements into BTNode structure"""
        
        # Determine node type based on tag name
        node_type = self._classify_node(element.tag)
        
        # Create BTNode
        node = BTNode(
            id=element.get('ID', element.tag),
            node_type=node_type,
            tag=element.tag,
            attributes=dict(element.attrib),
            children=[],
            parent=parent,
            depth=depth,
            path=self._generate_path(element, parent)
        )
        
        # Parse children
        for child_element in element:
            if child_element.tag in ['BehaviorTree']:
                continue  # Skip nested tree definitions
                
            child_node = self._parse_element(child_element, node, depth + 1)
            node.children.append(child_node)
        
        self.all_nodes.append(node)
        return node
    
    def _classify_node(self, tag: str) -> NodeType:
        """Classify node type based on XML tag"""
        if tag in self.CONTROL_NODES:
            return NodeType.CONTROL
        elif tag in self.DECORATOR_NODES:
            return NodeType.DECORATOR
        elif tag == 'SubTree':
            return NodeType.SUBTREE
        elif tag == 'Condition':
            return NodeType.CONDITION
        elif tag.startswith('Action') or tag == 'AlwaysSuccess' or tag == 'AlwaysFailure':
            return NodeType.ACTION
        else:
            # Default classification - could be custom nodes
            return NodeType.ACTION
    
    def _generate_path(self, element: ET.Element, parent: Optional[BTNode]) -> str:
        """Generate a unique path for the node including sibling index"""
        if parent is None:
            return element.tag
        
        # Count siblings with the same tag to create unique paths
        parent_element = element.getparent() if hasattr(element, 'getparent') else None
        sibling_index = 0
        
        if parent_element is not None:
            # Count siblings of the same tag that come before this element
            for sibling in parent_element:
                if sibling == element:
                    break
                if sibling.tag == element.tag:
                    sibling_index += 1
        
        # Include node ID or attributes for more uniqueness
        node_id = element.get('ID', '')
        if node_id:
            return f"{parent.path}/{element.tag}[@ID='{node_id}']"
        else:
            return f"{parent.path}/{element.tag}[{sibling_index}]"
    
    def get_tree_structure(self, tree_id: str = None) -> List[str]:
        """Get a text representation of the tree structure"""
        if tree_id is None:
            tree_id = list(self.trees.keys())[0] if self.trees else None
            
        if tree_id not in self.trees:
            return ["Tree not found"]
            
        root = self.trees[tree_id]
        result = []
        self._build_structure_text(root, result, "")
        return result
    
    def _build_structure_text(self, node: BTNode, result: List[str], prefix: str):
        """Recursively build text representation of tree structure"""
        # Create node description
        attrs_str = ""
        if node.attributes:
            key_attrs = ['ID', 'name', 'sub_tree_name', 'service_name']
            important_attrs = {k: v for k, v in node.attributes.items() if k in key_attrs}
            if important_attrs:
                attrs_str = " " + " ".join(f'{k}="{v}"' for k, v in important_attrs.items())
        
        node_desc = f"{prefix}├─ {node.tag}({node.node_type.value}){attrs_str}"
        result.append(node_desc)
        
        # Process children
        for i, child in enumerate(node.children):
            is_last = i == len(node.children) - 1
            child_prefix = prefix + ("   " if is_last else "│  ")
            self._build_structure_text(child, result, child_prefix)
    
    def get_node_statistics(self) -> Dict[str, int]:
        """Get statistics about the parsed trees"""
        stats = {
            'total_trees': len(self.trees),
            'total_nodes': len(self.all_nodes),
            'control_nodes': sum(1 for n in self.all_nodes if n.node_type == NodeType.CONTROL),
            'action_nodes': sum(1 for n in self.all_nodes if n.node_type == NodeType.ACTION),
            'condition_nodes': sum(1 for n in self.all_nodes if n.node_type == NodeType.CONDITION),
            'decorator_nodes': sum(1 for n in self.all_nodes if n.node_type == NodeType.DECORATOR),
            'subtree_nodes': sum(1 for n in self.all_nodes if n.node_type == NodeType.SUBTREE),
            'max_depth': max(n.depth for n in self.all_nodes) if self.all_nodes else 0
        }
        return stats