import sys
import os
import csv
import codecs

def output_clean_data(prediction_dataPath, hanzi_datapath, out_pos_file, out_neg_file, out_clean_pos_hanzi_txt, out_clean_neg_hanzi_txt):
    out_pos_Hler = open(out_pos_file, 'w')
    out_neg_Hler = open(out_neg_file, 'w')
    hanzi_datapath_hler = codecs.open(hanzi_datapath, 'rb', 'utf-8')
    all_hanzi_data = hanzi_datapath_hler.readlines()
    out_clean_pos_hanzi_hler = codecs.open(out_clean_pos_hanzi_txt,'wb', 'utf-8')
    out_clean_neg_hanzi_hler = codecs.open(out_clean_neg_hanzi_txt,'wb', 'utf-8')
    i = 0
    with open(prediction_dataPath) as f:
        rdr = csv.reader(f, delimiter=',', quotechar='"')
        for row in rdr:
            label = float(row[1])
            if label > 0:
                out_pos_Hler.write(row[0]+'\n')
                out_clean_pos_hanzi_hler.write(all_hanzi_data[i])
            elif label < 1.0:
                out_neg_Hler.write(row[0]+'\n')
                out_clean_neg_hanzi_hler.write(all_hanzi_data[i])
            i += 1
                    
    out_pos_Hler.close()
    out_neg_Hler.close()
    out_clean_pos_hanzi_hler.close()
    out_clean_neg_hanzi_hler.close()
    hanzi_datapath_hler.close()
                  
   
if __name__ == '__main__':
    output_clean_data(sys.argv[1], sys.argv[2], sys.argv[3],sys.argv[4], sys.argv[5],sys.argv[6])
