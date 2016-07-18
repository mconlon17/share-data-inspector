# SHARE Data Inspector

A very simple data inspector for SHARE.  Using elasticSearch, query the SHARE database for each provider and for each 
field of an abstract create work to determine the "field density" -- the percentage of fields that have values.  So,
for example, if a title is missing for a work as supplied by a provider, the field density for title for that provider 
would be less than 1.0.  1.0 is a perfect score, the field always has a value.  0.0 indicates the provider never provides
a value for that field.

See SAMPLE.txt for sample output.

## Suggestions for next steps

1. Rewrite using sharepa
1. Create visualizations and drill downs to missing data
1. Inspect entities beyond AbstractCreativeWork