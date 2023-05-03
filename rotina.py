import subprocess

# Start first program
p1 = subprocess.Popen(['python', 'iniciador_de_string.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Wait for both programs to finish
out1, err1 = p1.communicate()

print('1')
# Start second program
p2 = subprocess.Popen(['python', 'gerador_de_string_cod_font.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


out2, err2 = p2.communicate()
print('2')
# Print output and errors
print(out1.decode())
print(out2.decode())
print(err1.decode())
print(err2.decode())

# Start first program
p3 = subprocess.Popen(['python', 'spider_links.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Wait for both programs to finish
out3, err3 = p3.communicate()
print('3')
p4 = subprocess.Popen(['python', 'spider_content.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

out4, err4 = p4.communicate()
print('4')
p5 = subprocess.Popen(['python', 'code_deleter.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out5, err5 = p5.communicate()
print('5')
p6 = subprocess.Popen(['python', 'code_infos.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out6, err6 = p6.communicate()
print('6')

output1 = subprocess.check_output(['python', 'code_plots.py'])

output1_values = output1.decode().strip().split(',')
avg = float(output1_values[0])
devpad = float(output1_values[1])
meddifsal = float(output1_values[2])
devpaddisp = float(output1_values[3])
# p7 = subprocess.Popen(['python', 'code_plots.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
subprocess.check_call(['python', 'plotagem.py', str(avg), str(devpad), str(meddifsal), str(devpaddisp)])

print('7')



# p8 = subprocess.Popen(['python', 'plotagem.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# out8, err8 = p8.communicate()
# print('8')