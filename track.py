#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Lou Viannay <lou@islandtechph.com>

import requests
import json
import datetime
import pytz

import cPickle as pickle


from pprint import PrettyPrinter

pp = PrettyPrinter()


url = "https://tracking.phlpost.gov.ph"
get_path = "/HOME/GetTrackingEventsJson"


cookies = {
    '_ga': 'GA1.3.261972643.151902355'
}

headers = {
    'content-type': 'application/json;charset=utf-8',
    'host': 'tracking.phlpost.gov.ph',
}


def map_status_code(status_code):
    status_code_map = ['35', '1107', '38', '31', '30', '8', '12', '1', '0']
    return status_code_map.index(status_code) \
        if status_code in status_code_map \
        else len(status_code_map) + 1


def sort_by_event(iterable):
    iterable.sort(key=lambda val: map_status_code(val['StatusCode']))


def get_datetime_fname(fname_pattern):
    d = datetime.datetime.now(pytz.timezone("Asia/Manila"))
    q = d.strftime("%Y%m%d%H%M%S%f")
    return fname_pattern.format(q)


def get_history(TrackingNumber):
    payload = {
        'TrackingNumber': str(TrackingNumber)
    }
    json_data = json.dumps(payload)
    # print json_data

    r = requests.post(
        url+get_path,
        data=json_data,
        cookies=cookies,
        headers=headers
    )

    # print r.text
    # print r.status_code
    data = {
        'status': r.status_code,
        'reason': r.reason,
    }
    if r.status_code == 200:
        data['payload'] = json.loads(r.text)
    else:
        data['payload'] = None

    return data


def track_numbers(tracking_numbers):
    url_path = "/HOME/GetSummary"
    payload_data = {"TrackingNos": tracking_numbers}
    payload = json.dumps(payload_data)
    # print payload

    try:
        r = requests.post(
            url+url_path,
            data=payload,
            cookies=cookies,
            headers=headers,
        )
        if r.status_code == 200:
            data = json.loads(r.text)
            # pp.pprint(data)
            return data['InqItems']
        else:
            print r.text
            print r.status_code
            return None
    except requests.exceptions.ConnectionError as e:
        print "Connection Error"
        print e
        return None


def read_data():
    data = {}
    with open("data.txt", "r") as f:
        for line in f:
            first, remainder = line.split(None, 1)
            data[first] = remainder.strip()
    return data


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("datafile", nargs="?", default=None,
                        help="data file to parse, instead of reading online")
    return parser.parse_args()


def main():
    # get_history()

    args = parse_args()

    data = read_data()

    if args.datafile:
        with open(args.datafile, "r") as f:
            res = pickle.load(f)

    else:
        # pp.pprint(data)

        tracking_numbers = list(data.keys())
        res = track_numbers(tracking_numbers)
        if res is None:
            print "Unable to connect"
            return 1

        fname = get_datetime_fname("tracking_{}.pkl")
        with open(fname, "w") as f:
            f.write(pickle.dumps(res))

    sort_by_event(res)

    for item in res:
        k = item['TrackingNumber']
        description = data[k]
        status = item['Status']
        status_code = item['StatusCode']
        date_string = item['StatusDateStrings']
        print "{:14} {:40} {:20}".format(
            k, description, date_string
        )
        print "{:>12}:  {}\n".format(
            status_code, status
        )

    # pp.pprint(res)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
