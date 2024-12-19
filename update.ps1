function update{
	param ($commit_message)

	git add --all
	git commit -m $commit_message
	git push origin main
}

update $args[0]