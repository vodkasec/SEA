"""
    This file is part of SEA.

    SEA is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SEA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with SEA.  If not, see <http://www.gnu.org/licenses/>.

    Copyright 2013 by neuromancer
"""

from core import *

from Function    import *
#from Common      import getValueFromCode
from TypeSlicer   import getTypedValue

class FuncParameters:
  def __init__(self):
    self.parameters = dict()
    
  def __str__(self):
    
    counters = self.parameters.keys()
    counters.sort()
    
    ret = "Parameters detected:"
    
    for c in counters:
      ret = ret + "\n" + str(c) + " -> "
      param_info = self.parameters[c]
      fname = param_info["function"]
      ret = ret + fname + "("
      
      for (l,t,p) in param_info["parameters"]:
        #print self.parameters[c]#["function"]
        ret = ret  + " " +  str(l) + " := " + str(t)+"@" + str(p) + ","
      ret = ret + ")"
    
    return ret
  
  def getParameters(self, counter):
    
    if counter in self.parameters:
      return self.parameters[counter]["parameters"]
    
    return None
    
  def detectFuncParameters(self, reil_code, memaccess, callstack, inputs, counter):
    
    ins = reil_code[-1]
    
    assert(ins.isCall() and ins.called_function <> None)
    
    # first we locate the stack pointer to know where the parameters are located
    esp_op = RegOp("esp","DWORD")
    (val,ptbase) = getTypedValue(reil_code, callstack, memaccess, esp_op, Type("Ptr32", None))
 
    #ptbase = getType(reil_code, callstack, memaccess, esp_op, Type("Ptr32", None)) 
    
    # we reset the path
    #reil_code.reverse()
    #reil_code.reset()
    
    #val = getValueFromCode(reil_code, callstack, inputs, memaccess, esp_op)
    #ptbase.addTag("offset", val)
    
    #if str(ptbase) == "Ptr32":
    #  print "Unable to detect arguments for", ins.called_function
    #  return
    
    func_cons = funcs.get(ins.called_function, Function)
    func = func_cons(pbase = (ptbase, val))
    #assert(0)
    parameters = []
    
    for (par_pt, memop, needed) in func.getParameterLocations():
      if needed:
      
        reil_code.reverse()
        reil_code.reset()
        
        (val,pt) = getTypedValue(reil_code, callstack, memaccess, memop, par_pt)

        #pt = getType(reil_code, callstack, memaccess, memop, par_pt)
        
        #reil_code.reverse()
        #reil_code.reset()
        
        #val = getValueFromCode(reil_code, callstack, inputs, memaccess, memop)
        #print  "parameter of",ins.called_function, "at", str(location) , "has value:", val.name
        parameters.append((memop, pt, val))
      else:
        parameters.append((None, None, None))
    
    if parameters <> []:
      self.parameters[counter] = self.__getParameters__(ins, parameters)
    

  def __getParameters__(self, ins, raw_parameters):
    parameters = dict()
    parameters["function"] = ins.called_function
    parameters["parameters"] = list(raw_parameters)
    parameters["address"]   = ins.address
    
    return parameters
