class ButtonStyles():
    def __init__(self):

        self.start= '''
                        QPushButton
                                {
                                    background-color:#32CD32;
                                    border-style: outset;
                                    border-width: 1px;
                                    border-color: green;
                                    border-radius:15px;                                
                                }
                                QPushButton:hover
                                {
                                    background-color:#90EE90;
                                }
                            '''
        self.stop= '''QPushButton
                                {
                                    background-color:red;
                                    border-style: outset;
                                    border-width: 1px;
                                    border-color: red;
                                    border-radius:15px;                                
                                }
                                QPushButton:hover
                                {
                                    background-color:lightred;
                                }
                            '''