import lexparse_bla
import sys

l_list = lexparse_bla.l_errors_list
p_list = lexparse_bla.p_errors_list
s_list = lexparse_bla.s_errors_list
printed = []


def l_errors(file_out):
	for item in l_list:
		file_out.write(item)
		print(item)


def p_errors(file_out):
	for item in p_list:
		file_out.write(item)
		print(item)

def s_errors(file_out):
	for item in s_list:
		file_out.write(item)
		print(item)


def main():
	input_filename = sys.argv[1]
	output_filename = input_filename[:input_filename.rfind('.')] + '.err'
	file_out = open(output_filename, mode='w')
	l_errors(file_out)
	if len(l_list) == 0:
		p_errors(file_out)
		if len(p_list) == 0:
			s_errors(file_out)
	file_out.close()
    
if __name__ == "__main__":
    main()


