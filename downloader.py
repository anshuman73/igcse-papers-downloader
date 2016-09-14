import os
import requests


def main():
	url = raw_input('\nPaste a XtremePapers Link (Must be a link of A Folder containing the files you want to Download) : ')

	try:
		url_req = requests.get(url)
		html = url_req.text
		html = html[html.find('Parent Directory'):]

		total_files = html[html.find('small">') + len('small">'): html.find('Files', html.find('small">'))]
		total_size = html[html.find("Total size:") + len("Total size: "): html.find('<', html.rfind("Total size"))]
		html = html[:html.find("Total size:")]
		if raw_input('\nDownload ' + total_files + ' Files worth ' + total_size + '? (Press Enter to Start or any other key to Abort): ') == '':
			count = 0
			while count != int(total_files):
				start = html.find('href=') + 5
				end = html.find('>', start)
				link = html[start + 1:end - 1]  # Done to remove the Quotes - '"'
				link = 'http://papers.xtremepapers.com' + link[2:]
				file_name = link[link.rfind('/') + 1:]
				folder_name = link[link.rfind('/', 0, link.rfind('/')) + 1: link.rfind('/')]
				file_size = html[html.find('autoindex_td_right">', end) + len('autoindex_td_right">'):html.find("<", html.find('autoindex_td_right">', end) + len('autoindex_td_right">'))]
				html = html[end:]
				local_path = os.getcwd() + '\\' + folder_name + '\\'

				if not os.path.exists(local_path):
					os.makedirs(local_path)

				file_req = requests.get(link, stream=True)

				if os.path.exists(local_path + file_name):
					online_size = int(file_req.headers['Content-Length'])
					local_size = os.path.getsize(local_path + file_name)
					if online_size == local_size:
						print 'File ' + str(count + 1) + ' of ' + total_files + ' "' + file_name + '" already exists, skipping...'
						count += 1
						continue

				print '\nDownloading File ' + str(count + 1) + ' of ' + total_files + ' "' + file_name + '" \t\tSize: ' + file_size

				local_file = open(local_path + file_name, 'wb')
				for block in file_req.iter_content(512):
					if not block:
						break
					local_file.write(block)

				count += 1

		if raw_input('\nPress Enter to use another link or any other key to exit: ') == '':
			main()
	except KeyboardInterrupt:
		print '\nStopped by the User. Exiting...'
	except:
		print '\nEither the Link is invalid or papers.xtremepapers.com is down. Please confirm by visiting XtremePapers yourself and try again.'
		main()

main()
