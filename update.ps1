function update{
	param ($commit_message)
	
	Get-ChildItem -Path .\export -Include *.* -File -Recurse | foreach {$_.Delete()}
	git add --all
	git commit -m $commit_message
	git push origin main
}

update $args[0]