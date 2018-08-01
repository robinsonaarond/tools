#! /bin/bash
###
# This gets the average frequency of checkins for each
# snitch to guess what its frequency should be.
#
# Depends on checks on a graphite host, for more complete history
#
# Intended to be run periodically and sent as an email.
###

# Globals
WHISPER_SNITCH_DIR=""
API_KEY=""

## Should come out as newline for each snitch with a pipe and then frequency, e.g.:
#
#  snitch1|daily
#  snitch2|weekly
#
##
#all_snitches_frequency=$(curl -s -u $API_KEY: https://api.deadmanssnitch.com/v1/snitches|egrep '(name|interval.*,)'|awk -F":" '{print $2}'|sed -e '$!N;s/\n/ /' -e 's/,//g' -e 's/"//g'| awk '{print $1 "|" $2}')
all_snitches_frequency=$(curl -s -u $API_KEY: https://api.deadmanssnitch.com/v1/snitches|tr '}' '\n'|grep 'SSv2'|grep interval|cut -d':' -f4,15,16,17,18,19|sed -e 's/"/ /g' -e 's/,/ /g' -e 's/:/ /g'|awk '{print $1"|"$NF}')

# Returns string of frequency in DMS
function get_snitch_frequency() {
	local snitch=$1
	for s in $all_snitches_frequency; do
		if [[ "$s" =~ .*$snitch.* ]]; then
			echo $(echo $s | cut -d '|' -f2)
			return 0
		fi
	done
	echo "unknown"
	return 0
}

pushd $WHISPER_SNITCH_DIR >/dev/null
	echo "DMS Frequency for snitch / Observed frequency over last 20 entries"
	for dir in *; do
		dms_frequency=$(get_snitch_frequency $dir)

        # Here we get average frequency of time between each entry in the whisper DB (back 26 occurrences)
		whisper-fetch $dir/checked_in_at.wsp |grep -v None|tail -n26|
			awk -v dir="$dir" -v dms_frequency=$dms_frequency '
				BEGIN {
					sum=0; 
					num=0
				} { 
					diff = $1 - prev1; 
					prev1 = $1; 
					if (diff > 120 && diff < 2000000) {
						sum += diff; 
						num+=1;
					}
				} END {
					if (sum > 0 && num > 0) {
						avg = sum/num; 
						if (avg < 2000) frequency = "15_minutes";
						else if (avg > 2000 && avg < 10000) frequency = "hourly";
						else if (avg > 10000 && avg < 800000 ) frequency = "daily";
						else if (avg > 800000) frequency = "weekly";
						if (frequency != dms_frequency) {
							printf "%-50s %-10s \n", dir, ": " dms_frequency " / " frequency ". (" num " checked)";
						}
					}
				}
			'
	done
popd >/dev/null
