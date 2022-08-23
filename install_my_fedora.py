import subprocess, re, json, sys
inst_file = 'install_file.json'
def get_software():
    cmds = 'dnf --userinstalled repoquery'
    patt = '[-][0-9][:].*\n'

    # выполняем команду os linux в терминале
    # сохраняем ее вывод в переменной output
    # так как вывод это tuple, сограняем только первый элемент
    # второй элемент содержит вывод ошибок
    # содержимое элемента - строка
    proc_run=subprocess.Popen(cmds, shell=True, text=bool, stdout=subprocess.PIPE)
    output = proc_run.communicate()[0]

    # разбиваем строку в список
    # согласно разделителю определенному как regex
    output_re=re.split(patt, output)
    # преобразем во множество, что избавиться от
    # дублирующих строк
    output_re = set(output_re)
    # преобразуем обратно в список
    # сортируем 
    # удаляем пустой элемент в начале списка
    output_re = list(output_re)
    output_re.sort()
    del output_re[0]
    # кодируем объект (список) в формат json
    # чтобы сохранить объект в файле
    out_json = json.dumps(output_re)
    # save to file
    f = open(inst_file, 'w')
    f.write(out_json)
    f.close()

def set_software():
    cmds = 'sudo dnf install '
    f = open(inst_file, 'r')
    inp_json = f.read()
    output = json.loads(inp_json)

    for packet in output:
        subprocess.run(cmds+packet, shell=True, text=bool)
    
    # proc_run=subprocess.Popen(cmds2, text=True, stdout=subprocess.PIPE)
    # output = proc_run.communicate()[0]
    # f = open(my_file, 'w')
    # f.write(output)
    # f.close()

if __name__ == '__main__':
    try:
        if sys.argv[1] == '-i':
            print('Installing software...')
            set_software()
        if sys.argv[1] == '-s':
            print('Getting software list...')
            get_software()
            print('OK. Software list saved in', inst_file)
    except:
        print('Error')
