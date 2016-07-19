# tweetpub
A tool for preparing annotated collections of tweets for publishing

TweetPub is a tool for preparation of Twitter data annotated on token level for publishing, given the restrictions of the Twitter Terms of Service. The tool consists of two scripts, one for encoding, the other for decoding.

You can try out the tool on a toy corpus available in ```janes.tweet.vert.toy```.

## Encoding

For encoding your Twitter corpus (annotated on token level) you should have your data in any format which has each token in one line, annotations being tab-separated. There can be structural annotation between tokens, they just can not have the same number of tab-delimited values as token lines.

An example of an annotated tweet in a viable format is this:

```
<text id="tid.392972411765018626" lang="slv" type="post" favorited="0" retweeted="0" user="007_de
lic" sex="female" source="private" year="2013" month="2013-10" date="2013-10-23" time="11:14:58" 
std_tech="T1" std_ling="L1" senti="neutral">
<p>
<s>
@rantman   @rantman   @rantman   Xa      Na      1-13
No      no      no      Q       L       15-16
<g/>
,       ,       ,       Z       U       17-17
toliko  toliko  toliko  Rgp     Rsn     19-24
o       o       o       Sl      Dm      26-26
tvojih  tvojih  tvoj    Agpnpl  Ppnsmm  28-33
jajcih  jajcih  jajce   Ncnpl   Sosmm   35-40
<g/>
.       .       .       Z       U       41-41
</s>
<s>
Oziroma oziroma oziroma Cc      Vp      43-49
njih    njih    on      Pp3mpg  Zotmmr  51-54
obstoju obstoju obstoj  Ncmsd   Somed   56-62
<g/>
.       .       .       Z       U       63-63
</s>
</text>
```

Notice that one of the attributes encoded with each token are its character positions in the original tweet. This attribute (together with a tweet ID) is necessary to reconstruct the corpus during decoding.

The encoding tool accepts a series of command line arguments: (1) (--ncol) the number of attributes in each token-encoding line (2) (--tokencol) the number of the column in which the original token is encoded and (3) (--to_encode) a list of column numbers that have to be encoded given the token.

An example run of the encoder, if the above data is stored in ```temp```, is this:

```
$ python encode_tweetpub.py --ncol 6 --tokencol 1 --to_encode 2 3 < temp

<text id="tid.392972411765018626" lang="slv" type="post" favorited="0" retweeted="0" user="007_delic" sex="female" source="private" year="2013" month="2013-10" date="2013-10-23" time="11:14:58" std_tech="T1" std_ling="L1" senti="neutral">
<p>
<s>
TOKEN   (0, u'', 0, u'') (0, u'', 0, u'')        Xa      Na      1-13
TOKEN   (1, u'n', 0, u'')       (1, u'n', 0, u'')       Q       L       15-16
<g/>
TOKEN   (0, u'', 0, u'')        (0, u'', 0, u'')        Z       U       17-17
TOKEN   (0, u'', 0, u'')        (0, u'', 0, u'')        Rgp     Rsn     19-24
TOKEN   (0, u'', 0, u'')        (0, u'', 0, u'')        Sl      Dm      26-26
TOKEN   (0, u'', 0, u'')        (0, u'', 2, u'')        Agpnpl  Ppnsmm  28-33
TOKEN   (0, u'', 0, u'')        (0, u'', 2, u'e')       Ncnpl   Sosmm   35-40
<g/>
TOKEN   (0, u'', 0, u'')        (0, u'', 0, u'')        Z       U       41-41
</s>
<s>
TOKEN   (1, u'o', 0, u'')       (1, u'o', 0, u'')       Cc      Vp      43-49
TOKEN   (0, u'', 0, u'')        (0, u'o', 3, u'')       Pp3mpg  Zotmmr  51-54
TOKEN   (0, u'', 0, u'')        (0, u'', 1, u'')        Ncmsd   Somed   56-62
<g/>
TOKEN   (0, u'', 0, u'')        (0, u'', 0, u'')        Z       U       63-63
</s>
</text>
```

As you can see from the output, the token values are replaced with a dummy ```TOKEN``` value while the values to be encoded are encoded in 4-tuples relative to the token value: ```(length_of_prefix,new_prefix,length_of_suffix,new_suffix)```. By applying the given rule on the token value, the value of the specific attribute is reconstructed. For instance, for the token ```jajcih``` the rule of the second encoded attribute is the following: ```(0, u'', 2, u'e')```. By removing two characters from the end of the string, and adding the new suffix, we are obtaining ```jajce```.

# Decoding

Once a user wants to decode the corpus to its original format, the ```decode_tweetpub.py``` script should be used.

Before running the script, the user should edit its top with (1) proper credentials for using the Twitter API (obtainable from https://apps.twitter.com) and (2) regular expressions matching the start of a tweet, the tweet ID obtainable from the starting line of a tweet and the ending of a tweet.

In the case of our encoding example, the start of a tweet is defined as ```r'^<text '```, the tweet ID as ```r'id="tid.(.+?)"'``` and the end of a tweet as ```r'^</text>'```.

The command line interface is similar to the one of the encoding script with the following arguments: (1) (--ncol) the number of attributes in each token-encoding line (2) (--tokencol) the number of the column in which the original token should be encoded (3) (--offsetcol) the number of the column in which the position of the token in the original tweet is encoded and (4) (--to_decode) a list of column numbers that have to be decoded given the token.

An example run of the decoder, if the encoded data is stored in ```temp2```, is this:

```
$ python decode_tweetpub.py --ncol 6 --tokencol 1 --offsetcol 6 --to_decode 2 3 < temp2
<text id="tid.392972411765018626" lang="slv" type="post" favorited="0" retweeted="0" user="007_de
lic" sex="female" source="private" year="2013" month="2013-10" date="2013-10-23" time="11:14:58" 
std_tech="T1" std_ling="L1" senti="neutral">
<p>
<s>
@rantman   @rantman   @rantman   Xa      Na      1-13
No      no      no      Q       L       15-16
<g/>
,       ,       ,       Z       U       17-17
toliko  toliko  toliko  Rgp     Rsn     19-24
o       o       o       Sl      Dm      26-26
tvojih  tvojih  tvoj    Agpnpl  Ppnsmm  28-33
jajcih  jajcih  jajce   Ncnpl   Sosmm   35-40
<g/>
.       .       .       Z       U       41-41
</s>
<s>
Oziroma oziroma oziroma Cc      Vp      43-49
njih    njih    on      Pp3mpg  Zotmmr  51-54
obstoju obstoju obstoj  Ncmsd   Somed   56-62
<g/>
.       .       .       Z       U       63-63
</s>
</text>
```

You should have patience during decoding as the Twitter API allows fetching 100 tweets every 15 seconds. The decoder has this time constraint hard-coded.
