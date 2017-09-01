# TweetPub

TweetPub is a tool for preparation of Twitter data annotated on token level for publishing, given the restrictions of the Twitter Terms of Service. The tool consists of two scripts, one for encoding, the other for decoding.

You can try out the tool on a toy corpus available in ```janes.tweet.vert.toy```.

## Encoding

For encoding your Twitter corpus (annotated on token level) you should have your data in any format which has each token in one line, annotations being tab-separated. There can be structural annotation between tokens, they just can not have the same number of tab-delimited values as token lines.

An example of an annotated tweet in a viable format is this:

```
<text id="tid.392972411765018626" type="tweet" lang="slv" favorited="0" retweeted="0" user="007_delic" source="private" sex="female" year="2013" month="2013-10" date="2013-10-23" time="11:14:58" std_tech="T1" std_ling="L1" sentiment="neutral">
<p>
<s>
<name type="per">
@NovakBozidar	@NovakBozidar	@NovakBozidar-n	Xa	Na	=	1-13
</name>
No	No	no-l	Q	L	=	15-16
<g/>
,	,	,-u	Z	U	=	17-17
toliko	toliko	toliko-r	Rgp	Rsn	=	19-24
o	o	o-d	Sl	Dm	=	26-26
tvojih	tvojih	tvoj-z	Ps2mpls	Zsdmmme	=	28-33
jajcih	jajcih	jajce-s	Ncnpl	Sosmm	=	35-40
<g/>
.	.	.-u	Z	U	=	41-41
</s>
<s>
Oziroma	Oziroma	oziroma-v	Cc	Vp	=	43-49
njih	njih	on-z	Pp3mpa	Zotmmt	=	51-54
obstoju	obstoju	obstoj-s	Ncmsd	Somed	=	56-62
<g/>
.	.	.-u	Z	U	=	63-63
</s>
<s>
Ciao	Ciao	Ciao-m	I	M	=	65-68
<g/>
!	!	!-u	Z	U	=	69-69
</s>
<s>
<name type="per">
@Delo	@Delo	@Delo-n	Xa	Na	=	71-75
</name>
</s>
</p>
</text>
```

Notice that one of the attributes encoded with each token are its character positions in the original tweet. This attribute (together with a tweet ID) is necessary to reconstruct the corpus during decoding.

The encoding tool accepts a series of command line arguments: (1) (--ncol) the number of attributes in each token-encoding line (2) (--tokencol) the number of the column in which the original token is encoded and (3) (--to_encode) a list of column numbers that have to be encoded given the token.

An example run of the encoder, if the above data is stored in ```temp```, is this:

```
$ python encode_tweetpub.py --ncol 7 --tokencol 1 --to_encode 2 3 < janes.tweet.vert.toy

<text id="tid.392972411765018626" type="tweet" lang="slv" favorited="0" retweeted="0" user="007_delic" source="private" sex="female" year="2013" month="2013-10" date="2013-10-23" time="11:14:58" std_tech="T1" std_ling="L1" sentiment="neutral">
<p>
<s>
<name type="per">
TOKEN	(0, u'', 0, u'')	(0, u'', 0, u'-n')	Xa	Na	=	1-13
</name>
TOKEN	(0, u'', 0, u'')	(1, u'n', 0, u'-l')	Q	L	=	15-16
<g/>
TOKEN	(0, u'', 0, u'')	(0, u'', 0, u'-u')	Z	U	=	17-17
TOKEN	(0, u'', 0, u'')	(0, u'', 0, u'-r')	Rgp	Rsn	=	19-24
TOKEN	(0, u'', 0, u'')	(0, u'', 0, u'-d')	Sl	Dm	=	26-26
TOKEN	(0, u'', 0, u'')	(0, u'', 2, u'-z')	Ps2mpls	Zsdmmme	=	28-33
TOKEN	(0, u'', 0, u'')	(0, u'', 2, u'e-s')	Ncnpl	Sosmm	=	35-40
<g/>
TOKEN	(0, u'', 0, u'')	(0, u'', 0, u'-u')	Z	U	=	41-41
</s>
<s>
TOKEN	(0, u'', 0, u'')	(1, u'o', 0, u'-v')	Cc	Vp	=	43-49
TOKEN	(0, u'', 0, u'')	(0, u'o', 3, u'-z')	Pp3mpa	Zotmmt	=	51-54
TOKEN	(0, u'', 0, u'')	(0, u'', 1, u'-s')	Ncmsd	Somed	=	56-62
<g/>
TOKEN	(0, u'', 0, u'')	(0, u'', 0, u'-u')	Z	U	=	63-63
</s>
<s>
TOKEN	(0, u'', 0, u'')	(0, u'', 0, u'-m')	I	M	=	65-68
<g/>
TOKEN	(0, u'', 0, u'')	(0, u'', 0, u'-u')	Z	U	=	69-69
</s>
<s>
<name type="per">
TOKEN	(0, u'', 0, u'')	(0, u'', 0, u'-n')	Xa	Na	=	71-75
</name>
</s>
</p>
</text>
```

As you can see from the output, the token values are replaced with a dummy ```TOKEN``` value while the values to be encoded are encoded in 4-tuples relative to the token value: ```(length_of_prefix,new_prefix,length_of_suffix,new_suffix)```. By applying the given rule on the token value, the value of the specific attribute is reconstructed. For instance, for the token ```jajcih``` the rule of the second encoded attribute is the following: ```(0, u'', 2, u'e-s')```. By removing two characters from the end of the string, and adding the new suffix, we are obtaining ```jajce-s```.

# Decoding

Once a user wants to decode the corpus to its original format, the ```decode_tweetpub.py``` script should be used.

Before running the script, the user should edit its top with (1) proper credentials for using the Twitter API (obtainable from https://apps.twitter.com) and (2) regular expressions matching the start of a tweet, the tweet ID obtainable from the starting line of a tweet and the ending of a tweet.

In the case of our encoding example, the start of a tweet is defined as ```r'^<text '```, the tweet ID as ```r'id="tid.(.+?)"'``` and the end of a tweet as ```r'^</text>'```.

The command line interface is similar to the one of the encoding script with the following arguments: (1) (--ncol) the number of attributes in each token-encoding line (2) (--tokencol) the number of the column in which the original token should be encoded (3) (--offsetcol) the number of the column in which the position of the token in the original tweet is encoded and (4) (--to_decode) a list of column numbers that have to be decoded given the token.

An example run of the decoder, if the encoded data is stored in ```janes.tweet.vert.toy.enc```, is this (the output can be found in ```janes.tweet.vert.toy.enc.dec```):

```
$ python decode_tweetpub.py --ncol 7 --tokencol 1 --offsetcol 7 --to_decode 2 3 < janes.tweet.vert.toy.enc
<text id="tid.392972411765018626" type="tweet" lang="slv" favorited="0" retweeted="0" user="007_delic" source="private" sex="female" year="2013" month="2013-10" date="2013-10-23" time="11:14:58" std_tech="T1" std_ling="L1" sentiment="neutral">
<p>
<s>
<name type="per">
@NovakBozidar	@NovakBozidar	@NovakBozidar-n	Xa	Na	=	1-13
</name>
No	No	no-l	Q	L	=	15-16
<g/>
,	,	,-u	Z	U	=	17-17
toliko	toliko	toliko-r	Rgp	Rsn	=	19-24
o	o	o-d	Sl	Dm	=	26-26
tvojih	tvojih	tvoj-z	Ps2mpls	Zsdmmme	=	28-33
jajcih	jajcih	jajce-s	Ncnpl	Sosmm	=	35-40
<g/>
.	.	.-u	Z	U	=	41-41
</s>
<s>
Oziroma	Oziroma	oziroma-v	Cc	Vp	=	43-49
njih	njih	on-z	Pp3mpa	Zotmmt	=	51-54
obstoju	obstoju	obstoj-s	Ncmsd	Somed	=	56-62
<g/>
.	.	.-u	Z	U	=	63-63
</s>
<s>
Ciao	Ciao	Ciao-m	I	M	=	65-68
<g/>
!	!	!-u	Z	U	=	69-69
</s>
<s>
<name type="per">
@Delo	@Delo	@Delo-n	Xa	Na	=	71-75
</name>
</s>
</p>
</text>
```

You should have patience during decoding as the Twitter API allows fetching 100 tweets every 15 seconds.
