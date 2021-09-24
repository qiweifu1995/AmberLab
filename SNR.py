import pandas as pd
import os
import glob
import logging
logging.basicConfig(format="%(message)s", level=logging.INFO)

FILE_DIRECTORY = r"D:\Users\Kiwi\Downloads\EXP AFA 210804-1/"
OUTPUT_NAME = "SNR Report.txt"
CHUNK_SIZE = 200
NOISE_WIDTH = 20
NUMBER_TEST = 100


def extract_snr(file_dir: str, chunk_size: int, noise_width, number_to_test: int):
    """main function to call to extract SNR of provided file directory"""
    output_list = []
    file_dir = file_dir
    if os.path.isdir(file_dir):
        # folder exist, now extract all the file with Droplet
        os.chdir(file_dir)
        logging.info("Current working directory confirmed: " + os.getcwd())
        file_list = get_list_of_files(file_dir)
        for file in file_list:
            #logging.info(file)
            output_df = pd.DataFrame(columns=["Noise Floor", "Peak", "SNR"])
            csv_file = pd.read_csv(file, header=None, nrows=chunk_size*number_to_test)
            # logging.info("CSV File INFO : " + str(csv_file.info()))
            for i in range(0, len(csv_file.index), chunk_size):
                # taking a front and back noise, smaller one will be taken
                df_holder = pd.DataFrame()
                noise_front = csv_file.iloc[i:i+noise_width].mean(axis=0)
                noise_back = csv_file.iloc[i+chunk_size-noise_width:i+chunk_size].mean(axis=0)
                noise = []
                for j in noise_front.index:
                    if noise_front[j] < noise_back[j]:
                        noise.append(noise_front[j])
                    else:
                        noise.append(noise_back[j])
                df_holder["Noise Floor"] = noise.copy()
                #logging.info(noise)
                df_holder["Peak"] = csv_file.iloc[i:i+chunk_size].max(axis=0)
                #logging.info("Mean Value: " + str(noise))
                #logging.info("Max Value: " + str(max_value))
                df_holder["SNR"] = df_holder["Peak"] / df_holder["Noise Floor"]
                output_df = output_df.append(df_holder)
            output_df = output_df.fillna(0)
            final_df = output_df.groupby(level=0)
            final_df = final_df.agg(["mean"])
            logging.info(final_df)
            output_list.append(file)
            output_list.append(str(final_df))
        with open(OUTPUT_NAME, 'w') as f:
            for output in output_list:
                f.write(output + '\n')
        f.close()




def get_list_of_files(file_dir: str):
    """function to return list of files to be analyzed"""
    file_list = [x for x in os.listdir(file_dir) if "Droplet Record.csv" in x]
    logging.info(file_list)
    return file_list



if __name__ == '__main__':
    extract_snr(FILE_DIRECTORY, CHUNK_SIZE, NOISE_WIDTH, NUMBER_TEST)