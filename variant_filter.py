# Process CSV into range objects
import csv

class AmpliconRange(object):
    def __init__(self, start, stop, amp_id):
        self.range_ = (int(start), int(stop))
        self.amp_id = amp_id

    def in_range(self, base_number):
        """
        Checks if base_number is in self.range_ from (start) to (stop) --> stop inclusive!
        """
        return (base_number in range(self.range_[0], self.range_[1]) )

    def __repr__(self):
        return str({self.amp_id: self.range_})


def read_amp_file(amp_file):
    range_objs = []
    with open(amp_file, 'rb') as amp_rdr:
        rdr = csv.DictReader(amp_rdr)
        for row in rdr:
            range_objs.append(AmpliconRange(
                amp_id=row['Amplicon_ID'],
                start=row['Amplicon_Start'],
                stop=row['Amplicon_Stop']
            ))

    return range_objs


def assign_amps(df, amps):
    """
    I hate pandas. i think its a great piece of whatever which is why everyone must be using it but who writes syntax like this ... who makes a data library so unintuitive and difficult to iterate through and modify values in. who makesit so hard to index specific columns in rows? i hate it. i want everyone to know i hate it. let it be known. Why does the documentation not have any examples at all. i'm stupid i cant figure this out. thats the whole reason that im at the documentation page right now. is everyone else really smart or just really quiet about how frustrating this library is.
    HALF the indexing and slicing methods dont work HALF THE time. every five seconds the type of the data youre working on will change into something else. last time a series type frame turned into a long long long short. thats really what happened. no slice methods worked on this at all. i.__dict__ returned an error. it devolved into a primative type
    Contact: slin63@illinois.edu
    """
    df = df.assign(amp=None)
    for index in df.index:

        where = tuple(df.loc[index][['CHR', 'POS']])
        amp_id = amp_sort(where[0], where[1], amps)
        df.loc[index, 'amp'] = amp_id

    return df


def amp_sort(chr, pos, amps):
    """get hype for this N^2 run time boys"""
    for amp in amps:
        if amp.in_range(pos):
            ret = amp.amp_id
            break

    return ret




def process_to_drop(drop_list, master_list, amps):
    """df = pandas.dataframe type object for the poor souls trying to understand this in the future"""
    to_assign = [drop_list, master_list]
    for i in range(len(to_assign)):
        to_assign[i] = assign_amps(to_assign[i], amps)

    ## TODO: Filtering stuff tiffany asked for.

    return drop_list

















# Debugging
if __name__ == '__main__':
    amp = 'ampliconregions.csv'
    read_amp_file(amp)
