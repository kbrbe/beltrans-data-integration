# ISNI



## Request data via the SRU API

There is a limited API with free access and one for members which returns more data fields and also records not yet with status assigned. The base URL is the same, but for the member version additional parameters have to be provided.

* free limited API https://isni-m.oclc.org/sru
* member API https://isni-m.oclc.org/sru/username=USER/password=PASSWORD/DB=1.3 (where proper values for USER and PASSWORD need to be provided).

According to the SRU explain record there is a limit of 1000 search results per request. How many records one would like to get can be set with the URL parameter `maximumRecords=x`.

There is also a `startRecord` parameter, thus one can download content in several badges using the following strategy:

1. use the member API in the browser with needed search terms, read the number of matches on top of the result page
2. request with parameters `startRecord=1&maxRecords=1000`
3. do further requests such as `startRecord=1001&maxRecords=1000` until all needed records are downloaded.

The response of one request looks like the following

```
<?xml version="1.0" encoding="iso-8859-1" ?>
<ZiNG:searchRetrieveResponse xmlns:ZiNG="urn:z3950:ZiNG:Service" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <ZiNG:resultSetId></ZiNG:resultSetId>
    <ZiNG:numberOfRecords>60452</ZiNG:numberOfRecords>
    <ZiNG:records>
    
        <ZiNG:record>
            <ZiNG:recordSchema>isni-e</ZiNG:recordSchema>
                <ZiNG:recordData>
                    <collection xmlns="http://www.loc.gov/MARC21/slim">
                        <record> ... </record

        <ZiNG:record>
<ZiNG:recordSchema>isni-e</ZiNG:recordSchema>
<ZiNG:recordData>
<collection xmlns="http://www.loc.gov/MARC21/slim">
<record> ... </record>
```

