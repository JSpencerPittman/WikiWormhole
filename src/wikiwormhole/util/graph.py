from typing import (Set,
                    List,
                    TypeVar,
                    Generic,
                    Dict,
                    Union,
                    cast)

NodeType = TypeVar('NodeType')

"""
TERMINOLOGY

emitting node: the node emitting(outgoing) one or more edges.
absorb node: the node absorbing(incoming) one or more edges.

A singular node can emit and absorb.
"""


class AbsorbNode(Generic[NodeType]):
    """
    This class represents an absorbtion node. 
    This class is used to discover which emitting nodes edges point to this node. 

    Args:
        Generic (NodeType): The type used to uniquely identify nodes.
    """

    def __init__(self, absorb_node: NodeType) -> None:
        """
        Constructor for GraphNode.

        Args:
            absorb_node (NodeType): the unique identifier of this absorbtion node.
            emit_node (NodeType): the emit node pointing to this absorption node. 
        """

        self._absorber = absorb_node

        self._num_cnxs: int = 0

    def new_connection(self, emit_node: NodeType) -> None:
        """
        Save the emitting node pointing to this absorption node.

        Args:
            emit_node (NodeType): the node from which the edge originates.
        """

        if self._num_cnxs == 0:
            self._first_emitter: NodeType = emit_node
            self._all_emitters: Set[NodeType] = {emit_node}
            self._num_cnxs = 1
        elif emit_node not in self._all_emitters:
            self._num_cnxs += 1
            self._all_emitters.add(emit_node)

    def absorber(self) -> NodeType:
        """
        Returns this node's unique identifier.

        Returns:
            NodeType: This node's unique identifier.
        """

        return self._absorber

    def total_connections(self) -> int:
        """
        Returns the number of unique emitting nodes that point to this node.

        Returns:
            int: The number of unique emitting nodes that point to this node.
        """

        return self._num_cnxs

    def first_emitter(self) -> Union[NodeType, None]:
        """
        Returns the first emitting node to point to this node.

        Returns:
            Union[NodeType, None]: The first emitting node to point to this node, or None of there are
              no connected nodes.
        """

        return self._first_emitter if self._num_cnxs > 0 else None

    def all_references(self) -> Union[Set[NodeType], None]:
        """
        Returns all emitting nodes that have pointed to this node.

        Raises:

        Returns:
            Union[Set[NodeType], None]: All emitting nodes that have pointed to this node, 
              or None of there are no connected nodes.
        """

        return self._all_emitters if self._num_cnxs > 0 else None


class ConnectionGraph(Generic[NodeType]):
    """
    This class implements a network graph of absorption nodes that is used to determine
    if two points are connected by a path.


    Args:
        Generic (NodeType): The type used to uniquely identify nodes.
    """

    def __init__(self, root_node: NodeType) -> None:
        """
        Constructor for ConnectionGraph.

        Args:
            root_node (NodeType): the root node from which all nodes will be connected to.
        """

        self._graph: Dict[NodeType, AbsorbNode[NodeType]] = {}
        self._root_node = root_node

    def new_connection(self, emit_node: NodeType, absorb_node: NodeType) -> None:
        """
        Adds a new edge in the search graph going from the emitting to the absorb node.

        Args:
            emit_node (NodeType): node emitting the edge.
            absorb_node (NodeType): node absorbing the edge.
        """

        if absorb_node not in self._graph.keys():
            self._graph[absorb_node] = AbsorbNode(absorb_node)

        self._graph[absorb_node].new_connection(emit_node)

    def node_exists(self, node: NodeType) -> bool:
        """
        Does the node exist?

        Args:
            node (NodeType): node we are checking for the existence.

        Returns:
            bool: does the node exist in the graph?
        """

        return node in self._graph.keys() or node == self._root_node

    def node(self, absorb_node: NodeType) -> Union[AbsorbNode, None]:
        """
        Retreives an absorption node from the network graph.

        Args:
            absorb_node (NodeType): unique identifier of the node.

        Returns:
            AbsorbNode: the requested absorption node, or None if it doesn't exist.
        """

        return self._graph[absorb_node] if self.node_exists(absorb_node) else None

    def unravel(self, target_node: NodeType) -> Union[List[NodeType], None]:
        """
        Find the path from the root node to the target node.

        Args:
            final_node (NodeType): the target node in the path.

        Returns:
             Union[List[NodeType], None]: a list of the nodes connecting the root to the path, 
                or None if the target node doesn't exist.
        """

        if not self.node_exists(target_node):
            return None

        trace = [target_node]
        curr_node: NodeType = target_node

        while curr_node != self._root_node:
            curr_node = cast(NodeType, self._graph[curr_node].first_emitter())
            trace.append(curr_node)

        return trace[::-1]

    def asorb_nodes(self) -> List[NodeType]:
        """
        Returns a list of all of the absorption nodes in the graph.

        Returns:
            List[NodeType]: A list of all of the absorption nodes in the graph.
        """

        return list(self._graph.keys())

    def __len__(self) -> int:
        return len(self._graph)
