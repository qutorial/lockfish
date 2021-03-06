from testing import *
from lockfish.clangparser import *
from lockfish.lazy import *
from lockfish.nodeutils import get_all_descendants
#test decls

rdr()
curs = parse('unittest/one.c').cursor
listit = curs.get_children()

td = []
for n in listit:
  td.append(n)
rdrstop()


class TestLazy(tc):

  #1
  def testPasrsing(self):
    call = td[2]
    self.assertTrue(call.spelling == 'b')

  #2
  def testInit(self):
    call = td[2]
    dg = get_all_descendants(call)
    self.assertTrue(dg.__class__ == ncl)

  #3
  def testFilter1(self):
    call = td[2]
    d = get_all_descendants(call)
    d = d.filter(lambda n: n.spelling == 'x')
    self.assertTrue(len(d.filters) == 1)
    i = 0
    for i, n in enumerate(d):
      self.assertTrue(i <= 2)
    self.assertTrue(i == 2)
  #4
  def testAny1(self):
    call = td[2]
    d = get_all_descendants(call)
    d = d.filter(lambda n: n.spelling == 'x')
    self.assertTrue(d.any(lambda n: n.kind == CursorKind.DECL_REF_EXPR) == True)

  #5
  def testIter(self):
    call = td[2]
    d = get_all_descendants(call)
    d = d.filter(lambda n: n.spelling == 'x')
    i = 0
    for c in d:
      self.assertTrue(c.kind == CursorKind.UNEXPOSED_EXPR or c.kind == CursorKind.PARM_DECL or c.kind == CursorKind.DECL_REF_EXPR)
      i+=1
    self.assertTrue(i==3)

  #6
  def testInit2(self):
    d = ncl(td)
    self.assertTrue(len (d.root) == 3 )

  #7
  def testInit3(self):
    d = ncl(curs)
    rdr()
    d.pprint()
    rdrstop()
    v = rdrval()
    self.assertTrue(len(v.splitlines()) >= 16)

  #8
  def testShallow(self):
    d = ncl(curs).ofkind(CursorKind.FUNCTION_DECL).tonc()
    self.assertTrue(d.count() == 3)

  def testDepth(self):
    d = ncl(curs).ofkind(CursorKind.VAR_DECL).tonc()
    self.assertTrue(d.count() == 1)
    d = ncl(curs).ofkind(CursorKind.VAR_DECL).maxdepth(0).tonc()
    self.assertTrue(d.count() == 0)
    d = ncl(curs).ofkind(CursorKind.VAR_DECL).maxdepth(1).tonc()
    self.assertTrue(d.count() == 0)
    d = ncl(curs).ofkind(CursorKind.VAR_DECL).maxdepth(2).tonc()
    self.assertTrue(d.count() == 0)
    d = ncl(curs).ofkind(CursorKind.VAR_DECL).maxdepth(3).tonc()
    self.assertTrue(d.count() == 0)
    d = ncl(curs).ofkind(CursorKind.VAR_DECL).maxdepth(4).tonc()
    self.assertTrue(d.count() == 1)
    d = ncl(curs).ofkind(CursorKind.VAR_DECL).maxdepth(5).tonc()
    self.assertTrue(d.count() == 1)

if  __name__ == '__main__':
    unittest.main()
