from github_manager import save_html, read_html

# Read your HTML
html_content = read_html('index.html')
print(html_content)

# Make changes to it
updated_html = html_content.replace('old text', 'new text')

# Save it back to GitHub
save_html('index.html', updated_html, 'Update HTML content')