import sqlite3
from database import lengths, data


class DictionaryToDatabase():
    def __init__(self):
        try:
            for d_dic in data.Movies:
                for l_dic in lengths.Movies:
                    if d_dic['Movie'] == l_dic['Movie']:
                        d_dic['Length'] = l_dic['Length'];

            for d_dic in data.Movies:
                if d_dic['Volume'] == '':
                    pass;
                else: d_dic['Volume'] = int(d_dic['Volume'])

            for d_dic in data.Movies:
                d_dic['Year'] = int(d_dic['Year']);
            print(*data.Movies[5:10], *lengths.Movies[2:7], sep='\n');

            self.db = sqlite3.connect("database.db");
            self.cursor = self.db.cursor();
            # Including source names
            # self.cursor.execute("CREATE TABLE dubs (Movie VARCHAR(250) PRIMARY KEY NOT NULL, Year Int NOT NULL, Length VARCHAR(250), Delay Int DEFAULT 0, Attenuation FLOAT DEFAULT 0.0, Volume Int DEFAULT 0, Source VARCHAR(250))");
            # Excluding source names (remove the last {} in cursor.execute() below)
            self.cursor.execute("CREATE TABLE dubs (Movie VARCHAR(250) PRIMARY KEY NOT NULL, Year Int NOT NULL, Length VARCHAR(250), Delay Int DEFAULT 0, Attenuation FLOAT DEFAULT 0.0, Volume Int DEFAULT 0)");
            for dic in data.Movies:
                if 'Length' in dic.keys():
                    pass;
                else: dic['Length'] = '';
                if type(dic['Delay']) == int:
                    dic['Delay'] = str(dic['Delay']);
                if type(dic['Attenuation']) == float:
                    dic['Attenuation'] = str(dic['Attenuation']);
                if type(dic['Volume']) == int:
                    dic['Volume'] = str(dic['Volume']);

            for dic in data.Movies:
                # I don't understand why, but using fstrings doesn't work with sqlite3. See below
                # self.cursor.execute(r'''INSERT OR IGNORE INTO dubs VALUES("{}", {}, "{}", "{}", "{}", "{}", "{}")'''.format(dic['Movie'], dic['Year'], dic['Length'], dic['Delay'], dic['Attenuation'], dic['Volume'], dic['Source']));

                # Excluding source names
                self.cursor.execute(r'''INSERT OR IGNORE INTO dubs VALUES("{}", {}, "{}", "{}", "{}", "{}")'''.format(dic['Movie'], dic['Year'], dic['Length'], dic['Delay'], dic['Attenuation'], dic['Volume']));
                # print(type(dic['Movie']), type(dic['Year']), type(dic['Length']), type(dic['Delay']), type(dic['Attenuation']), type(dic['Volume']));
                self.db.commit();
        except sqlite3.OperationalError: pass;
        print('done');
