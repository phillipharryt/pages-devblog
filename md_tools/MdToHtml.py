

class MdToHtml:
    
    def parse_headers(input_line: str):
        """
        #### Inputs:
            -@input_line: one line of markdown text
        #### Expected Behaviour:
            - header lines in markdown are delineated by lines starting with # characters (hashes)
            - If the line is empty or has no header hash, not relevant, return untouched
            - if it has header hashes then count them up to use in the h tag, 
                take the text after the hashes and put it inside the h tag
            - return this html text 
        #### Returns:
            - input_line with any headers converted to html
        """
        if(len(input_line) == 0 or input_line[0] != '#'):
            return(input_line)
        else:
            count = 0
            while count < len(input_line) and input_line[count] == '#':
                count += 1
            text_after_hashes = input_line.partition('#' * count)[2]
            header_text = f'<h{str(count)}>{text_after_hashes}</h{str(count)}>'
            return(header_text)
    
    
    def parse_alternate_headers(input_line: str, prior_line: str) -> str | tuple[str, str]:
        """
        #### Inputs:
            -@input_line: a line of markdown text
            -@prior_line: the line before that in the text 
        #### Expected Behaviour:
            - header lines can also be delineated by a line of = (equals) or - (dash) characters
                succeeding it 
            - for each input_line, if it's empty it can't be made of equals or dashes, return 
                both the inputs 
            - if the line is entirely made up of = or -, then return the previous line 
                inside the header tag
        #### Returns:
            - Either a single string, (if a header was parsed), or the two inputs returned 
                back if they're untouched
        """
        if(len(input_line) == 0):
            return(input_line, prior_line)

        stripped_line = input_line.strip()
        if(input_line.count('=') == len(stripped_line)):
            return(f'<h1>{prior_line}</h1>')
        elif(input_line.count('-') == len(stripped_line)):
            return(f'<h2>{prior_line}</h2>')
        else:
            return(input_line, prior_line)
            
    
    def parse_paragraphs(input_text: str) -> str:
        """
        #### Inputs:
            -@input_text: a full markdown section of text
        #### Expected Behaviour:
            - paragraphs are delineated by empty lines before and after them. 
        """
        return_lines = []
        blank_count = 0
        for line in input_text.splitlines():
            if(len(line.strip()) == 0):
                if(blank_count % 2 == 0):
                    return_lines.append('<p>')
                else: 
                    return_lines.append('</p>')
                blank_count += 1
            else:
                return_lines.append(line)
        return('\n'.join(return_lines))
            
        