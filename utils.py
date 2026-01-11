import sys
import os
from datetime import date
from bs4 import BeautifulSoup
from copy import deepcopy

class Post:
    filename: str
    title: str
    description: str
    publish_date: date
    
    def __init__(self):
        pass
    def load_from_html_file(self, filename: str):
        """
        #### Inputs:
            -@filename: name of .html file
        #### Expected Behaviour:
            - Open up the html file, load up the title and subtitle using the h1 and h2
            - get the custom timestamp tag, this is added to the publish_date
                so they can be sorted chronologically
        #### Returns:
            - None
        #### Side Effects:
            - populates the filename, title, description, publish_date on the instance
        """
        self.filename = filename
        with open(filename, 'r') as r:
            file_soup = BeautifulSoup(r, 'html.parser')
            
        title = file_soup.h1
        if not title:
            raise Exception(f'No h1 tag found in {filename}, this tag is required to title the post') 
        self.title = title.get_text()
        
        description = file_soup.h2
        if not description:
            raise Exception(f'No h2 tag found in {filename}, this tag is required to description the post')
        self.description = description.get_text()
        
        timestamp = file_soup.timestamp
        if timestamp is None:
            raise Exception(f'"{filename}" file lacks timestamp tag, posts cannot be ordered without one')
        date_text = timestamp.get_text()
        dd,mm,yyyy = date_text.split('/')
        date_instance = date(int(yyyy),int(mm),int(dd))
        self.publish_date = date_instance
        

class Category:
    name: str 
    posts: list[Post]
    def __init__(self, name: str):
        self.name = name
        self.posts = []
        
    def populate_posts_list(self):
        """
        #### Inputs:
            - None
        #### Expected Behaviour:
            - loop through the files inside the category's folder (ignoring its home page)
            - instatiate and populate Post objects for each one of these files
            - add these instances to the Category's post list
        #### Returns:
            - None 
        #### Side Effects:
            - modifies the self.posts attribute
        """
        for post_file in os.listdir(f'posts/{self.name}'):
            if(post_file == f'{self.name}.html'):
                continue
            new_post = Post()
            new_post.load_from_html_file(f'posts/{self.name}/{post_file}')
            self.posts.append(new_post)
        
class Utils:
    
    GITHUB_URL: str
            
    @staticmethod       
    def build_category_list() -> list[Category]:
        """
        #### Inputs:
            - None
        #### Expected Behaviour:
            - only works if there is a posts directory
            - each directory in the 'posts' directory is considered a category of posts 
                so they are looped over and a Category object is instantiated for each dir 
            - for each Category instance the posts within it are used to populate its posts attribute
        #### Returns:
            - list of Category instances with their .posts populated
        #### Side Effects:
            - None
        """
        if 'posts' not in os.listdir():
            raise Exception('"posts" directory required for compilation')
        category_directories = os.listdir('posts')
        category_list : list[Category] = []
        for category_directory in category_directories:
            new_category = Category(category_directory)
            new_category.populate_posts_list()
            category_list.append(new_category)
        return(category_list)


    @staticmethod
    def write_html(html_soup: BeautifulSoup, filename: str) -> None:
        """
        #### Inputs:
            -@html_soup: BeautifulSoup instance
            -@filename: place to write the html to 
        #### Expected Behaviour:
            - prettify and write to the filename
        """
        prettier = html_soup.prettify()
        with open(filename, 'w') as w:
            w.write(prettier)
            
    def build_sidebar_soup(self, category_list: list[Category]) -> BeautifulSoup:
        """
        #### Inputs:
            -@category_list: list of Category instances
        #### Expected Behaviour:
            - Construct a sidebar with a link to the homepage
            - loop through the categories and for each one add a link to the sidebar
            - return this as a BeautifulSoup instance
        #### Returns:
            - BeautifulSoup instance for the sidebar
        #### Side Effects:
            - None
        """
        sidebar_string = f"""
        <div class="sidebar no-print">
            <h2><a href="{self.GITHUB_URL}/index.html">Home</a><h2>
            <h3>Categories</h3>
        </div>
        """
        sidebar_soup = BeautifulSoup(sidebar_string, 'html.parser')
        div = sidebar_soup.div
        for category in category_list:
            sidebar_link = sidebar_soup.new_tag('a')
            sidebar_link['href'] = f'{self.GITHUB_URL}/posts/{category.name}/{category.name}.html'
            sidebar_link.string = category.name
            div.append(sidebar_link)
        return(sidebar_soup)


    @staticmethod
    def add_sidebar_to_html_file(html_filename: str, sidebar_soup: BeautifulSoup) -> None:
        """
        #### Inputs:
            -@html_filename: file to add the sidebar to
            -@sidebar_soup: BeatifulSoup of siderbar (result of build_sidebar_soup)
        #### Expected Behaviour:
            - find the body of the file, within this find an existing sidebar
            - if there is an existing sidebar overwrite it with the incoming one,
                else, add the sidebar to the end of the body
        #### Returns:
            - None 
        #### Side Effects:
            - Writes to the html_filename 
        """
        with open(html_filename, 'r') as r:
            root = BeautifulSoup(r, 'html.parser')
        body = root.body
        if body == None:
            return
        existing_sidebar = body.find_all('div', {'class': 'sidebar'})
        if len(existing_sidebar):
            existing_sidebar[0].replace_with(deepcopy(sidebar_soup))
        elif sidebar_soup.contents:
            print('opp2')
            body.append(deepcopy(sidebar_soup))
            print('now')
            print(sidebar_soup)
        else:
            raise Exception('here')
        Utils.write_html(root, html_filename)
            
        
    @staticmethod
    def add_sidebar_to_all_posts(sidebar_soup: BeautifulSoup) -> None:
        """
        #### Inputs:
            -@sidebar_soup: BeautifulSoup instance of the sidebar (result of build_sidebar_soup)
        #### Expected Behaviour:
            - for each post nested in the posts folder, add the sidebar to the html
            - then also add it to the main index.html page
        #### Returns:
            - None 
        #### Side Effects:
            - Writes to all html files in posts folder, and in the index.html file
        """
        for category_dir in os.listdir('posts'):
            for file in os.listdir(f'posts/{category_dir}'):
                print('before')
                print(sidebar_soup)
                Utils.add_sidebar_to_html_file(f'posts/{category_dir}/{file}', sidebar_soup)
                print('after')
                print(sidebar_soup)
        Utils.add_sidebar_to_html_file('index.html', sidebar_soup)



    def generate_category_page(self, category: Category) -> None:
        """
        #### Inputs:
            -@category: single Category instance 
        #### Expected Behaviour:
            - Generate the framework of the html for the page, including stylesheet and name 
                (sidebar is done elsewhere)
            - for each post, add them as links with title and subtitle in the content section
        #### Returns:
            - None 
        #### Side Effects:
            - Creates or modifies a page in category folder
        """
        html_string = f"""
        <html>
            <head>
                <link rel="stylesheet" href="../../tufte.css"/>
                <link rel="stylesheet" href="../../custom.css"/>
            </head>
            <body>
            <div class="content">
                <h1>{category.name}</h1><hr><br>
            </div>
        </html>
        """
        html_soup = BeautifulSoup(html_string, 'html.parser')
        category.posts.sort(key=lambda x: x.publish_date, reverse=True)
        for post in category.posts:
            post_string = f"""
            <h3>
                <a href="{self.GITHUB_URL}/{post.filename}">{post.title}</a>
            </h3>
            <h4>{post.description}</h4>
            <br/>
            """
            post_soup = BeautifulSoup(post_string, 'html.parser')
            content_node = html_soup.find('div', {'class': 'content'})
            content_node.append(post_soup)
        Utils.write_html(html_soup, f'posts/{category.name}/{category.name}.html')


    @staticmethod
    def add_stylesheet_to_html_file(html_filename: str, stylesheet_path: str) -> None:
        """
        This is going to be different for the index instead of the root, maybe need to pass in the stylesheet path
        """
        with open(html_filename, 'r') as r:
            root = BeautifulSoup(r, 'html.parser')
        html = root.html
        existing_head = html.find('head')
        stylesheet_string = f'<link href="{stylesheet_path}" rel="stylesheet"/>'
        stylesheet_soup = BeautifulSoup(stylesheet_string, 'html.parser')
        if existing_head:
            existing_stylesheet = existing_head.find('link', {'href': stylesheet_path})
            if(existing_stylesheet):
                return
            else:
                existing_head.append(stylesheet_soup)
        else:
            head_string = f'<head>{stylesheet_string}</head>'
            head_soup = BeautifulSoup(head_string, 'html.parser')
            html.body.append(head_soup)
        Utils.write_html(root, html_filename)
        
        
    def add_stylesheet_to_all_files():
        base_tufte = 'tufte.css'
        base_custom = 'custom.css'
        Utils.add_stylesheet_to_html_file('index.html', base_tufte)
        Utils.add_stylesheet_to_html_file('index.html', base_custom)
        for category in os.listdir('posts'):
            for file in os.listdir(f'posts/{category}'):
                Utils.add_stylesheet_to_html_file(f'posts/{category}/{file}', f'../../{base_tufte}')
                Utils.add_stylesheet_to_html_file(f'posts/{category}/{file}', f'../../{base_custom}')
                
    
    def add_recent_posts_to_homepage(self):
        """
        Go through all posts, order them, pick the first 10 and add them to the main page 
        under 'Recent articles' 
        """
        all_posts = []
        for dir in os.listdir('posts'):
            for post in os.listdir(f'posts/{dir}'):
                if(post == f'{dir}.html'):
                    continue
                new_post = Post()
                new_post.load_from_html_file(f'posts/{dir}/{post}')
                all_posts.append(new_post)        
        all_posts.sort(key=lambda x: x.publish_date, reverse=True)
        max_posts = 10
        if len(all_posts) < 10:
            max_posts = len(all_posts)
        top_10 = all_posts[:max_posts]
        with open('index.html', 'r') as r:
            root = BeautifulSoup(r, 'html.parser')
        existing_recent_posts_header = root.find('div', {'id': 'recentposts'})
        if(existing_recent_posts_header):
            existing_recent_posts_header.decompose()
        recent_post_wrapper = BeautifulSoup('<div id="recentposts"></div>', 'html.parser')
        recent_posts_header = BeautifulSoup('<h2>Recent Posts</h2>', 'html.parser')
        recent_post_wrapper.div.append(recent_posts_header)
        for post in top_10:
            post_string = f"""
            <h3>
                <a href="{self.GITHUB_URL}/{post.filename}">{post.title}</a>
            </h3>
            <h4>{post.description}</h4>
            <br/>
            """
            post_soup = BeautifulSoup(post_string, 'html.parser')
            recent_post_wrapper.div.append(post_soup)
            
        content = root.find('div', {'class': 'content'})
        content.append(recent_post_wrapper)    
        Utils.write_html(root, 'index.html')
    
        