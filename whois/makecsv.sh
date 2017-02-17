echo nickname > nick.csv && awk -F, '{print $2}' info.csv | sort | uniq >> nick.csv
echo identd > identd.csv && awk -F, '{print $5}' info.csv | sort | uniq >> identd.csv
echo hostname > hostname.csv && awk -F, '{print $4}' info.csv | sort | uniq >> hostname.csv
echo realname > realname.csv && awk -F, '{print "rn-" $6}' info.csv | sort | uniq >> realname.csv
echo channel > channel.csv && awk -F, '{print $1 "-" $3}' chan.csv | sort | uniq >> channel.csv
echo network > network.csv && awk -F, '{print $1}' info.csv | sort | uniq >> network.csv
echo mode > mode.csv && awk -F, '{print $5}' chan.csv | sort | uniq >> mode.csv

echo "nickname,identd" > nickidentd.csv && awk -F, '{print $2 "," $5}' info.csv | sort | uniq >> nickidentd.csv
echo "nickname,hostname" > nickhostname.csv && awk -F, '{print $2 "," $4}' info.csv | sort | uniq >> nickhostname.csv
echo "nickname,realname" > nickrealname.csv && awk -F, '{print $2 "," "rn-" $6}' info.csv | sort | uniq >> nickrealname.csv
echo "nickname,channel" > nickchannel.csv && awk -F, '{print $2 "," $1 "-" $3}' chan.csv | sort | uniq >> nickchannel.csv
echo "nickname,network" > nicknetwork.csv && awk -F, '{print $2 "," $1 "-" $1}' chan.csv | sort | uniq >> nicknetwork.csv
echo "network,channel" > networkchannel.csv && awk -F, '{print $1 "," $1 "-" $3}' chan.csv | sort | uniq >> networkchannel.csv
echo "hostname,channel" > hostnamechannel.csv && awk -F, '{print $4 "," $1 "-" $3}' chan.csv | sort | uniq >> hostnamechannel.csv
echo "channel,mode" > modechannel.csv && awk -F, '{print $1 "-" $3 "," $5}' chan.csv | sort | uniq >> modechannel.csv


sed -i 's/\"//g' realname.csv
sed -i 's/\"//g' nickrealname.csv
