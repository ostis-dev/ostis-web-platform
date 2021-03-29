import sys
import os


def main(work_directory):
    list_of_files = list()
    for (dir_path, dir_names, file_names) in os.walk(work_directory):
        list_of_files += [os.path.join(dir_path, file) for file in file_names]
    for file in list_of_files:
        if file.endswith(".scs"):
            is_file_processed = False
            buffer_file_list = []
            with open(file, 'r', encoding='utf-8') as scs_file:
                dir_path = os.path.split(file)[0]
                for scs_file_line in scs_file:
                    if scs_file_line.find('[*^"file://') >= 0:
                        edit_line_list = scs_file_line.split('^"file://')
                        tabulation_string = ""
                        for _ in edit_line_list[0]:
                            tabulation_string = tabulation_string + " "

                        buffer_file_list.append(edit_line_list[0] + '\n')
                        scsi_path = edit_line_list[1].split('"*];;')[0]

                        relative_path = ""
                        if scsi_path.find('/') >= 0:
                            scsi_path_list = scsi_path.split('/')
                            for i in range(len(scsi_path_list) - 1):
                                relative_path = scsi_path_list[i] + '/'

                        with open(os.path.join(dir_path, scsi_path), 'r', encoding='utf-8') as scsi_file:
                            for scsi_file_line in scsi_file:
                                if scsi_file_line.find(r'"file://') >= 0 and len(relative_path) > 0:
                                    scsi_file_line = scsi_file_line[:scsi_file_line.find('//')+2] + \
                                                     relative_path + scsi_file_line[scsi_file_line.find('//')+2:]
                                buffer_file_list.append(tabulation_string + scsi_file_line)

                        buffer_file_list.append("\n")
                        buffer_file_list.append("*];;")
                        os.remove(os.path.join(dir_path, scsi_path))
                        is_file_processed = True
                    else:
                        buffer_file_list.append(scs_file_line)
            if is_file_processed:
                with open(file, "w", encoding="utf_8") as scs_file:
                    for scs_file_line in buffer_file_list:
                        scs_file.write(scs_file_line)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("invalid number of arguments, Please specify only the work directory")
