from llvmlite import ir
from ctypes import CFUNCTYPE, c_int
import llvmlite.binding as llvm
import m_parse_bla
import sys

tree = m_parse_bla.result
last_var = ""
var_dict = {}

def code_gen(tree): # traverse tree recursively to generate code
    global last_var
    if tree[0] == "Program":
        for t in tree[1:]:
            code_gen(t)
    elif tree[0] == "=":
        last_var = tree[1][1]
        var_dict[last_var] = builder.alloca(ir.IntType(32))
        builder.store(code_gen(tree[2]), var_dict[last_var])
    elif tree[0] == "A":
        return(builder.add(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "S":
        return(builder.sub(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "M":
        return(builder.mul(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == "D":
        return(builder.sdiv(code_gen(tree[1]),code_gen(tree[2])))
    elif tree[0] == 'BINARY_LITERAL':
        return(ir.Constant(ir.IntType(32), int(tree[1], 2)))
    elif tree[0] == 'ID':
        print("3rd")
        print(tree)
        return(builder.load(var_dict[tree[1]]))
    elif tree[0].isnumeric():
        return(ir.Constant(ir.IntType(32), int(tree, 2)))
    elif "Program" in tree[0]:
        for t in tree[0][1:]:
            code_gen(t)

inttyp = ir.IntType(32) # create int32 type
fnctyp = ir.FunctionType(inttyp, ()) # create function type to return a float
module = ir.Module(name="bla") # create module named "lang"
func = ir.Function(module, fnctyp, name="main") # create "main" function
block = func.append_basic_block(name="entry") # create block "entry" label
builder = ir.IRBuilder(block) # create irbuilder to generate code
code_gen(tree) # call code_gen() to traverse tree & generate code
builder.ret(builder.load(var_dict[last_var])) # specify return value

def main():
	input_filename = sys.argv[1]
	output_filename = input_filename[:input_filename.rfind('.')] + '.ir'
	file_out = open(output_filename, mode='w')
	file_out.write(str(module).strip())
	file_out.close()
	print(str(module).strip())

if __name__ == "__main__":
    main()