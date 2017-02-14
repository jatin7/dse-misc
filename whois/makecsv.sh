echo nick > nick.csv && awk -F, '{print $2}' info.cql | sort | uniq >> nick.csv
echo identd > identd.csv && awk -F, '{print $5}' info.cql | sort | uniq >> identd.csv
echo hostname > hostname.csv && awk -F, '{print $4}' info.cql | sort | uniq >> hostname.csv
echo realname > realname.csv && awk -F, '{print "rn-" $6}' info.cql | sort | uniq >> realname.csv
echo channel > channel.csv && awk -F, '{print $1 "-" $3}' chan.cql | sort | uniq >> channel.csv
echo network > network.csv && awk -F, '{print $1}' info.cql | sort | uniq >> network.csv
echo mode > mode.csv && awk -F, '{print $5}' chan.cql | sort | uniq >> mode.csv

echo "nick,identd" > nickidentd.csv && awk -F, '{print $2 "," $5}' info.cql | sort | uniq >> nickidentd.csv
echo "nick,hostname" > nickhostname.csv && awk -F, '{print $2 "," $4}' info.cql | sort | uniq >> nickhostname.csv
echo "nick,realname" > nickrealname.csv && awk -F, '{print $2 "," "rn-" $6}' info.cql | sort | uniq >> nickrealname.csv
echo "nick,channel" > nickchannel.csv && awk -F, '{print $2 "," $1 "-" $3}' chan.cql | sort | uniq >> nickchannel.csv
echo "nick,network" > nicknetwork.csv && awk -F, '{print $2 "," $1 "-" $3}' chan.cql | sort | uniq >> nicknetwork.csv
echo "network,channel" > networkchannel.csv && awk -F, '{print $1 "," $1 "-" $3}' chan.cql | sort | uniq >> networkchannel.csv
echo "channel,mode" > modechannel.csv && awk -F, '{print $1 "-" $3 "," $5}' chan.cql | sort | uniq >> modechannel.csv


sed -i 's/\"//g' realname.csv
sed -i 's/\"//g' nickrealname.csv
