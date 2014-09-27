"""
  Contains BFS and CC algorithms.
"""

from collections import deque

def bfs_visited(ugraph, start_node):
  """Executes BFS from start_node on ugraph, returning set of all reachable nodes."""
  theq = deque()
  theq.append(start_node)
  ret = set([start_node])
  while len(theq):
    start = theq.popleft()
    for neigbor in ugraph[start]:
      if neigbor not in ret:
        ret.add(neigbor)
        theq.append(neigbor)
  return ret

def cc_visited(ugraph):
  """Returns list of all connected components in ugraph."""
  nodes = set(ugraph.keys())
  components = []
  while len(nodes):
    node = nodes.pop()
    ccomp = bfs_visited(ugraph, node)
    components.append(ccomp)
    nodes = nodes - ccomp
    print "nodes: ", nodes, " cc: ", ccomp
  return components

def largest_cc_size(ugraph):
  """Returns the size of the largest component in ugraph."""

  return max([0]+[len(item) for item in cc_visited(ugraph)])


def compute_resilience(ugraph, attack_order):
  """Computes resilence of the network."""

  ret = [largest_cc_size(ugraph)]
  for node in attack_order:
    print node, " => ", ugraph
    del ugraph[node]
    for item in ugraph.itervalues():
      if node in item:
        item.remove(node) 
    ret.append(largest_cc_size(ugraph))
  return ret
