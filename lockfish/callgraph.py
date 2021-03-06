def getStack(node, stack):
  if node is None:
    return stack
  stack.insert(0, node)
  return getStack(node.back, stack)

class CGNode:
  def __init__(self):
    self.node = None
    self.children = []
    self.back = None
    self.recursed = False
    self.analyzed = False

  def pprint(self):
    print(self.spell())

  def spell(self):
    if self.node is None:
      return("None")
    else:
      return(self.node.spelling)

  def __str__(self):
    return self.spell()

  def __repr__(self):
    return self.spell()

  def __eq__(self, other):
    if self is None or other is None or self.node is None or other.node is None:
      return False
    if self.spell() == other.spell():
      return True

  def __ne_(self, other):
    return not self == other

  def addChild(self, n):
    self.children.append(n)
    n.back = self

  def getStack(self):
    return getStack(self, [])


def makeNode(n):
  res = CGNode()
  res.node = n
  return res

def printTree(root, offset):
  print offset, "|-", root.spell()
  for c in root.children:
    printTree(c, offset + "   ")

def find(root, filter):
  if filter(root):
    return root
  for c in root.children:
    r = find(c, filter)
    if r is not None:
      return r
  return None

def findShallow(root, filter):
  if filter(root):
    return root
  for c in root.children:
    if filter(c):
      return c
  for c in root.children:
    r = findShallow(c, filter)
    if r is not None:
      return r
  return None

def findAllFilter(root, filter):
  res = []
  if filter(root):
    res.append(root)
  for c in root.children:
    r1 = findAllFilter(c, filter)
    res += r1
  return res

def getPathInternal(root, node, path):
  path.append(root)
  if root == node:
    return path
  for c in root.children:
    r = getPathInternal(c, node, path)
    if r is not None:
      return r
  return None

def getPath(root, node):
  return getPathInternal(root, node, [])

def acceptVisitor(node, visitor):
  if node is not None:
    visitor.visit(node)
  for c in node.children:
    acceptVisitor(c, visitor)

class CallGraph:
  def __init__(self):
    self.root = CGNode()

  def pprint(self):
    printTree(self.root, "")

  def findFilter(self, filter):
    return find(self.root, filter)

  def findShallowFilter(self, filter):
    return findShallow(self.root, filter)

  def findByName(self, name):
    return self.findFilter(lambda x: x.spell() == name)

  def findByNameShallow(self, name):
    return self.findShallowFilter(lambda x: x.spell() == name)

  def find(self, node):
    return find(self.root, lambda n: n is node)

  def any(self, filter):
    return self.findFilter(filter) is not None

  def getPossiblePath(self, node):
    return getPath(self.root, node)

  def findAllFilter(self, filter):
    return findAllFilter(self.root, filter)

  def findAll(self, node):
    return self.findAllFilter(lambda n: n == node)

  def getLeaves(self):
    return self.findAllFilter(lambda n: len(n.children) == 0)

  def acceptVisitor(self, visitor):
    return acceptVisitor(self.root, visitor)


  def addCall(self, callee, caller):
    # check if exactly this call already exists
    if self.any(lambda n: n is caller):
      print "Call already exists:", caller.spell(), "calling", caller.getStack()
      return False

    # find the callee node in the tree
    calleeInTheTree = self.find(callee)
    # one has to add callee first
    if calleeInTheTree is None:
      print "No callee in the tree:", callee.spell()
      return False
    # check that there is no such caller already
    for c in calleeInTheTree.children:
      if c == caller:
        print "callee already exists:", c.spell(), "calling", calleeInTheTree.spell()
        return False
    # not building loops
    stack = calleeInTheTree.getStack()
    adding = True
    recursionFound = False
    for call in stack:
      # comparison by name here
      if not recursionFound and call == caller:
        recursionFound = True
        caller.recursed = True
        continue
      # chain closed already
      if recursionFound and call == caller:
        adding = False
        print "Recursion found on:", caller.spell(), "in stack", stack
    if adding:
      calleeInTheTree.addChild(caller)
      return True
    else:
      return False

  def getAllNames(self):
    v = GetAllNamesVisitor()
    self.acceptVisitor(v)
    return v.names

class GetAllNamesVisitor:
  def __init__(self):
    self.names = []
  def visit(self, node):
    if node is None:
      return
    if node.spell() in self.names:
      return
    else:
      self.names.append(node.spell())

