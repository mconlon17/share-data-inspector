#!/usr/bin/env/python

"""
    share_data_inspector.py -- Read SHARE data, provide a table of field value presence by provider

    Add additional SHARE entities from the API with fields to inspect for each.
    Rewrite using sharepa when it is upgraded to SHARE 2.0
    Show output in visualizations rather than a table

"""
import requests
import json

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2016 (c) Michael Conlon"
__license__ = "Apache License 2.0"
__version__ = "0.01"

query = '''
{
    "query": {
        "match" : {
            "title" : "genomics"
        }
    }
}
'''
query_form = '''
{
    "aggs": {
        "sources": {
            "significant_terms": {
                "percentage": {},
                "size": 0,
                "min_doc_count": 1,
                "field": "sources"
            }
        }
    },
    "query": {
        "bool": {
            "must_not": [
                {
                    "exists": {
                        "field": "{{}}"
                    }
                }
            ]
        }
    }
}
'''

# do not include auto generate fields date_modified, date, date_created, sources, @type

fields = ["associations", "links", "contributors", "tags", "date_updated", "title", "description",
        "venues", "language", "awards", "date_published", "subject"]
np = {}
for field in fields:
    query = query_form.replace('{{}}', field)
    headers = {"Content-Type": "application/json"}
    query_result = requests.post('https://staging-share.osf.io/api/search/abstractcreativework/_search',
                                headers=headers, data=query)
    query_doc = json.loads(query_result.text)
    print field, query_doc
    for bucket in query_doc["aggregations"]["sources"]["buckets"]:
        provider = bucket['key']
        docs = bucket['doc_count']
        total = bucket['bg_count']
        if provider not in np:
            np[provider] = {}
        if field not in np[provider]:
            np[provider][field] = {}
        np[provider][field]['docs'] = docs
        np[provider][field]['total'] = total
        np[provider][field]['pct'] = float(docs)/float(total)
print 'Raw Data'
print np
print
print "Field value presence by provider"
short_fields = []
column_width = 8
for field in fields:
    if len(field) < column_width:
        short_fields.append(field.rjust(column_width))
    else:
        short_fields.append(field[0:column_width])
print "                              ", ' '.join(short_fields)
for provider in sorted(np):
    print provider.ljust(30),
    for field in fields:
        if field not in np[provider]:
            val = 1.0
        else:
            val = 1.0 - np[provider][field].get('pct', 0.0)
        print "   %0.3f" % val,
    print

