import csv 

class CsvToHtmlMd():
    
    def __init__(self):
        pass
    
    # @staticmethod
    # def convert_csv_file_to_html_file(csv_filename: str, html_filename: str) -> None:
    #     """
    #     #### Inputs:
    #         -@csv_filename: filename to pull the csv data from (with extension)
    #         -@html_filename: resulting filename to write to (with extension)
    #     #### Expected Behaviour:
    #         - pass the file to convert_csv_file_to_html_string
    #         - prettify (somewhat) the result using prettify_table_html
    #         - save the result to .html file
    #     #### Returns:
    #         - None 
    #     #### Side Effects:
    #         - Writes to the html_filename
    #     """
    #     html_string = CsvToHtmlMd.convert_csv_file_to_html_string(csv_filename)
    #     pretty_html = CsvToHtmlMd.prettify_table_html(html_string)
    #     with open(html_filename, 'w') as w:
    #         w.write(pretty_html) 
    
    
    @staticmethod
    def convert_csv_file_to_html_string(csv_filename: str) -> str:
        """
        #### Inputs:
            -@csv_filename: filename to pull the csv data from (with extension)
        #### Expected Behaviour:
            - If file is found, open up, load all rows into a dict, 
            - The first row is considered headers
            - construct a header row with <th> tags using the headers ^ 
            - for element in the remaning rows, construct a cell for it using <td>
            - cap off the html and return it
        #### Returns:
            - html string of a table
        #### Side Effects:
            - None 
        """
        csv_data = []
        with open(csv_filename, 'r') as r:
            reader = csv.reader(r)
            for row in reader:
                csv_data.append(row)
        headers = csv_data[0]
        table_string = '<html><body><table><tr>'
        header_string = ''.join([f'<th>{val}</th>' for val in headers])
        table_string += header_string + '</tr>'
        for row in csv_data[1:]:
            row_string = '<tr>' + ''.join([f'<td>{val}</td>' for val in row]) + '</tr>'
            table_string += row_string
        table_string += '</table></body></html>'
        return(table_string)
    
    
    @staticmethod
    def prettify_table_html(ugly_string: str) -> str:
        """
        #### Inputs:
            -@ugly_string: expected to be html string
        #### Expected Behaviour:
            - Puts newline characters after values in the newline_list 
                to make the result slightly more readable
        #### Returns:
            - string after newlines are added in 
        #### Side Effects:
            - None 
        """
        pretty_string = ugly_string
        newline_list = ['<html>', '<body>', '<table>', '</tr>', '</table>', '</body>']
        for old in newline_list:
            pretty_string = pretty_string.replace(old, f'{old}\n')
        return(pretty_string)
        