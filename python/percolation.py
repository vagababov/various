import random
import math

__author__ = 'Victor Agababov'


class OutOfBounds(Exception):
  def __init__(self, n, i):
    self.n = n
    self.i = i

  def __str__(self):
    return '{0} is out of bounds [0..{1}]'.format(self.i, self.n)


class UF:
  """UF implements UnionFind, or DisjointSet data structure.
     See: https://en.wikipedia.org/wiki/Disjoint-set_data_structure
  """

  def __init__(self, n):
    """Initializes UF with given size.
    
    Args:
      n: the size of structure, must be positive.
    """
    if n <= 0:
      raise Exception('size must be positive, was: {0}'.format(n))
    self.data = [i for i in xrange(0, n)]
    self.ranks = [0]*n
    self.components = n

  def __len__(self):
    """Returns the size of the object."""
    return len(self.data)


  def Find(self, i):
    """Returns the identifier of the parent of object i.
       Find is compressing paths, i.e. mutating internal state.

    Args:
      i: the identifier whose parent must be found.
    Returns:
      the identifier of the parent.
    """
    if i < 0 or i >= len(self.data):
      raise OutOfBounds(len(self.data), i)
    if self.data[i] != i:
      self.data[i] = self.Find(self.data[i])
    return self.data[i]

  def Union(self, i, j):
    """Unionizes components identified by i and j, if they aren't unionized already.

    Args:
      i, j: components to unionize.
    """
    
    if i < 0 or i >= len(self.data):
      raise OutOfBounds(len(self.data), i)
    if j < 0 or j >= len(self.data):
      raise OutOfBounds(len(self.data), j)
    if i == j:
      return
    # Find roots.
    iRoot = self.Find(i)
    # If roots are the same, then we're done.
    jRoot = self.Find(j)

    # Otherwise hang smaller tree to the root of the bigger (deeper) tree.
    if iRoot != jRoot:
      self.components -= 1
      if self.ranks[iRoot] < self.ranks[jRoot]:
        self.data[iRoot] = jRoot
      else:
         self.data[jRoot] = iRoot
         # If trees had same size then parent's depth has to be increased by 1.
         if self.ranks[iRoot] == self.ranks[jRoot]:
           self.ranks[iRoot] += 1

  def num_components():
    """Returns number of independent components in the structure.

    Returns:
      integer in the [1, len(self)] range denoting number of components.
    """
    return self.components

  def __str__(self):
    return '{0} components: {1} -> {2}'.format(self.components, self.data, self.ranks)

  

class Percolator:
  """Implements percolation simulation for a square matrix of size n."""
  def __init__(self, n):
    """Initializes the Percolator object.
    
    Args:
      n: the size of the matrix dimension.
    """
    if n <= 1:
      raise Exception('n must be at least 2, was: {0}'.format(n))
    self.n = n
    self.field = [[False]*n for i in xrange(0, n)]
    self.uf = UF(n*n+2)
  
  def open(self, i, j):
    """Opens the element at coordinates i and j:

    Args:
      i: row
      j: column
    """
    if i < 0 or i >= self.n:
      raise OutOfBounds(self.n, i)
    if j < 0 or j >= self.n:
      raise OutOfBounds(self.n, j)
    # Already open
    if self.field[i][j]:
      return
    self.field[i][j] = True
    # Linear position of the (i, j) element for UF algorithm.
    p = i*self.n+j
    # For all 4 neigbours within matrix. If they are open Union them.
    for di, dj in zip((0, 0, 1, -1), (-1, 1, 0, 0)):
      ni, nj = i + di, j+dj
      if ni >= 0 and ni < self.n and nj >= 0 and nj < self.n:
        if self.field[ni][nj]:
          self.uf.Union(p, ni*self.n+nj)
    # If topmost row, then union with the source.
    if i == 0:
      self.uf.Union(p, self.n**2)
    # If bottom row, then union with the sink.
    if i == self.n-1:
      self.uf.Union(p, self.n**2+1)

  def is_open(self, i, j):
    """Returns is position at coordinates i and j is open.

    Args:
      i: row
      j: column
    Returns:
      True if the position is open.
    """
    if i < 0 or i >= self.n:
      raise OutOfBounds(self.n, i)
    if j < 0 or j >= self.n:
      raise OutOfBounds(self.n, j)
    return self.field[i][j]

  def is_full(self, i, j):
    """Returns true if position at coordinates i and j is full, i.e. connected to the source.

    Args:
      i: row
      j: column
    Returns:
      True if position is full.
    """
    if i < 0 or i >= self.n:
      raise OutOfBounds(self.n, i)
    if j < 0 or j >= self.n:
      raise OutOfBounds(self.n, j)

    if not self.field[i][j]:
      return False
    p = i*self.n + j
    return self.uf.Find(p) == self.uf.Find(self.n**2)

  def percolates(self):
    """Returns true if field currently percolates, i.e. there is a path from source to sink.

    Returns:
      True if field percolates.
    """
    p = self.n**2
    return self.uf.Find(p) == self.uf.Find(p+1)
    


def Percolate(n):
  """Percolate simulates percolation of field n.

  Args:
    n: the size of the field dimension.
  Returns:
    Percolator object
    Number of sites that had to be open for field to percolate.
  """
  random.seed()
  p = Percolator(n)
  num = 0
  while not p.percolates():
    i = random.randint(0, n-1)
    j = random.randint(0, n-1)
    if p.is_open(i, j):
      continue
    num += 1
    p.open(i, j)
  return p, num


def PercoStats(n, t):
  """Percolates field of size n, t times and returns mean, stddev and confidence interval of percolation probability,
      i.e. what fraction of sites has to be open in order for field to percolate.

  Args:
    n: size of the field.
    t: number of trials
  Returns:
    mean: mean fraction of sites required to be open for field to percolation
    stddev: standard deviation of said fraction values
    conf_int: tuple containing range for 95% confidence interval.
  """
  s = []
  size = n*n
  for i in xrange(0, t):
    x, num = Percolate(n)
    s.append(num/float(size))
  mean = sum(s)/float(t)
  print "Mean: ", mean
  stddev = 0.
  for x in s:
    stddev += (x-mean)**2
  stddev = math.sqrt(stddev/(t-1))
  print "StdDev: ", stddev
  ds = stddev*1.96/math.sqrt(t)
  conf_int = (mean-ds, mean+ds)
  print "95% Confidence interval: ", conf_int
  return mean, stddev, conf_int

