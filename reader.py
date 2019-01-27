import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_time
from dateutil.tz import tzlocal

class Reader:

    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    def __init__(self):
        print "in __init__!"
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', Reader.scope)
        client = gspread.authorize(creds)

        # Find a workbook by name and open the first sheet
        # Make sure you use the right name here.
        self.sheet = client.open("Musicjerk's big album sheet").sheet1
        self.latest_update_check = datetime.now(tzlocal())
        self.latest_update = None
        self.update_values()

    def update_required(self):
        if datetime.now(tzlocal()) - self.latest_update_check < timedelta(seconds = 5):
            print "Recently checked for updates!"
            return False
        latest_change_time = parse_time(self.sheet.cell(1, 1).value)
        print self.sheet.cell(1, 1).value
        self.latest_update_check = datetime.now(tzlocal())
        print "Update required: " + str(self.latest_update < latest_change_time)
        return self.latest_update < latest_change_time

    def update_values(self):
        print "Updating values from google sheets"
        self.latest_update = datetime.now(tzlocal())
        all_values   = self.sheet.get_all_values()
        top_row      = all_values[0]
        col_headers  = all_values[1]
        self.general_data = {}
        self.user_data    = {}
        self.albums       = []
        for row in all_values[2:]:
            album        = row[0]
            if not album:
                break                                        # Break since no more albums present
            self.albums.append(album)
            artist       = row[1]
            chosen_by    = row[2]
            average      = row[3]
            best_tracks  = row[4]
            worst_tracks = row[5]
            name = ""
            for col, value in enumerate(row[7:]):
                col    = col + 7
                name   = top_row[col].lower() if top_row[col] else name
                header = col_headers[col]
                if name not in self.user_data:
                    self.user_data[name] = {}
                if album not in self.user_data.get(name):
                    self.user_data[name][album] = {}
                self.user_data[name][album][header] = value

    @property
    def names(self):
        return self.user_data.keys()


    def generate_fig(self, name):
        fig, ax = plt.subplots()

        index = range(0, 11)
        bar_width = 0.7
        opacity = 0.4

        print "Attempting to generate fig for %s!" % name
        ratings = [self.user_data[name][album]['Rating'] for album in self.albums if album in self.user_data[name]]
        ratings = [int(rating) for rating in ratings if rating != ""]
        counts  = [0] * 11
        for rating in ratings:
            counts[rating] += 1

        rects1 = ax.bar(index, counts, bar_width,
                        alpha=opacity, color='b')

        ax.set_xlabel('Rating')
        ax.set_ylabel('Amount')
        ax.set_title(name.title() + "'s Ratings")
        ax.set_xticks([float(i) + bar_width/2 for i in index])
        ax.set_xticklabels(list(map(str, index)))
        ax.set_ylim(bottom = -0.5, top = 20.5)
        ax.set_xlim(left = -0.5, right = 11.5)
        fig.tight_layout()
        plt.savefig("data/%s.png" % name, bbox_inches='tight')
        #plt.show()

    #while True:
    #    name = raw_input('Whose ratings do you want to see?\n').lower()
    #    if name in user_data:
    #        generate_fig(name)
    #    else:
    #        print ("No data for '%s'" % name)
