# This is just part of documentation:
# A signature is a tuple of strings (each an affix).
# Signatures is a map: its keys are signatures.  Its values are *sets* of stems.
# StemToWord is a map; its keys are stems.       Its values are *sets* of words.
# StemToSig  is a map; its keys are stems.       Its values are individual signatures.
# WordToSig  is a Map. its keys are words.       Its values are *lists* of signatures.
# StemCounts is a map. Its keys are words. 	 Its values are corpus counts of stems.
# SignatureToStems is a dict: its keys are tuples of strings, and its values are dicts of stems.

class CWordList:
    def __init__(self):
        self.mylist = list()
       
    def GetCount(self):
        return len(self.mylist)
    def AddWord(self, word):
        self.mylist.append(Word(word))

    def at(self, n):
        return self.mylist[n]

    def sort(self):
        self.mylist.sort(key=lambda item: item.Key)
        # for item in self.mylist:
        #	print item.Key
        for i in range(len(self.mylist)):
            word = self.mylist[i]
            word.leftindex = i
        templist = list()
        for word in self.mylist:
            thispair = (word.Key[::-1], word.leftindex)
            templist.append(thispair)
        templist.sort(key=lambda item: item[0])
        for i in range(len(self.mylist)):
            (drow, leftindex) = templist[i]
            self.mylist[leftindex].rightindex = i

    def PrintXY(self, outfile):
        Size = float(len(self.mylist))
        for word in self.mylist:
            #print ("41", word.Key)
            x = word.leftindex / Size
            y = word.rightindex / Size
            print("{:20s} {:9.5} {:9.5}".format(word.Key, x, y), file = outfile)


class CLexicon:
    def __init__(self):
        self.WordList = CWordList()
        self.WordDictCounts = dict()

        self.Signatures = {}
        self.SignatureToStems = {}
        self.WordToSig = {}
        self.StemToWord = {}
        self.StemToAffixDict = {}
        self.StemCounts = {}
        self.StemToSig = {}
        self.Suffixes={}
        self.Prefixes = {}
        self.MinimumStemsInaSignature = 1
        self.MinimumStemLength = 5
        self.MaximumAffixLength =3
        self.MaximumNumberOfAffixesInASignature = 10
        self.NumberOfAnalyzedWords = 0
        self.LettersInAnalyzedWords = 0
        self.NumberOfUnanalyzedWords = 0
        self.LettersInUnanalyzedWords = 0
        self.TotalLetterCountInWords = 0
        self.LettersInStems = 0
        self.AffixLettersInSignatures = 0

        self.TotalRobustInSignatures = 0

    def PrintWordList(self, outfile):
        self.WordList.PrintXY(outfile)

    def Multinomial(self,this_signature):
        counts = dict()
        total = 0.0
        #print "{:45s}".format(this_signature), 
        for affix in this_signature:
            #print "affix", affix            
            counts[affix]=0
            for stem in self.SignatureToStems[this_signature]:      
                #print "stem", stem  
                if affix == "NULL":
                    word = stem
                else:
                    word = stem + affix
                #print stem,":", affix, "::", word
                #print "A", counts[affix], self.WordDictCounts[word]
                counts[affix] += self.WordDictCounts[word]
                total += self.WordDictCounts[word]
        frequency = dict()
        for affix in this_signature:
            frequency[affix] = counts[affix]/total
            #print "{:12s}{:10.2f}   ".format(affix, frequency[affix]),
        #print 


class Word:
    def __init__(self, key):
        self.Key = key
        self.leftindex = -1
        self.rightindex = -1


def byWordKey(word):
    return word.Key


class CSignature:
    count = 0

    def __init__(self):
        self.Index = 0
        self.Affixes = tuple()
        self.StartStateIndex = CSignature.count
        self.MiddleStateIndex = CSignature.Count + 1
        self.EndStateIndex = CSignature.count + 2
        CSignature.count += 3
        self.StemCount = 1

    def Display(self):
        returnstring = ""
        affixes = list(self.Affixes)
        affixes.sort()
        return "-".join(affixes)

        # ------------------------------------------------------------------------------------------##------------------------------------------------------------------------------------------#


class parseChunk:
    def __init__(self, thismorph, rString, thisedge=None):
        # print "in parsechunk constructor, with ", thismorph, "being passed in "
        self.morph = thismorph
        self.edge = thisedge
        self.remainingString = rString
        if (self.edge):
            self.fromState = self.edge.fromState
            self.toState = self.edge.toState
        else:
            self.fromState = None
            self.toState = None
            # print self.morph, "that's the morph"
            # print self.remainingString, "that's the remainder"

    def Copy(self, otherChunk):
        self.morph = otherChunk.morph
        self.edge = otherChunk.edge
        self.remainingString = otherChunk.remainingString

    def Print(self):
        returnstring = "morph: " + self.morph
        if self.remainingString == "":
            returnstring += ", no remaining string",
        else:
            returnstring += "remaining string is " + self.remainingString
        if self.edge:
            return "-(" + str(self.fromState.index) + ")" + self.morph + "(" + str(
                self.toState.index) + ") -" + "remains:" + returnstring
        else:
            return returnstring + "!" + self.morph + "no edge on this parsechunk"


            # ----------------------------------------------------------------------------------------------------------------------------#


class ParseChain:
    def __init__(self):
        self.my_chain = list()

    def Copy(self, other):
        for parsechunk in other.my_chain:
            newparsechunk = parseChunk(parsechunk.morph, parsechunk.remainingString, parsechunk.edge)
            self.my_chain.append(newparsechunk)

    def Append(self, parseChunk):
        # print "Inside ParseChain Append"
        self.my_chain.append(parseChunk)

    def Print(self, outfile):
        returnstring = ""
        columnwidth = 30
        for i in range(len(self.my_chain)):
            chunk = self.my_chain[i]
            this_string = chunk.morph + "-"
            if chunk.edge:
                this_string += str(chunk.edge.toState.index) + "-"
            returnstring += this_string + " " * (columnwidth - len(this_string))
        print >> outfile, returnstring,
        print >> outfile

    def Display(self):
        returnstring = ""
        for i in range(len(self.my_chain)):
            chunk = self.my_chain[i]
            returnstring += chunk.morph + "-"
            if chunk.edge:
                returnstring += str(chunk.edge.toState.index) + "-"
        return returnstring

        # ----------------------------------------------------------------------------------------------------------------------------#
class CAlternation:
    def __init__(self, stemcount = 0):
        self.Alloforms = list() # list of CAlloforms
        self.Count = stemcount
        
    def AddAlloform(self, this_alloform):
            self.Alloforms.append(this_alloform)

    def MakeProseReportLine(self):
        ReportLine = CProseReportLine()


        return ReportLine.MakeReport( )


    def display(self):
        this_datagroup = CDataGroup("KeyAndList",self.Count)         
        for i in range(len(self.Alloforms)):
            alloform = self.Alloforms[i]
            this_datagroup.Count = self.Count
            if alloform.Form ==  "":
                key = "nil" 
            else:
                key = alloform.Form
            if key not in this_datagroup.MyKeyDict:
                this_datagroup.MyKeyDict[key]=list()
            this_datagroup.MyKeyDict[key].append(alloform.Context)
         
        return this_datagroup.display()

 #       for i in range(len(self.Alloforms)):
 #         

#            return_string = ""
#            alloform = self.Alloforms[i]
#            if alloform.Form ==  "":
#                key = "nil" 
#            else:
#                key = alloform.Form
#            this_datagroup.MyListOfKeys.append(key)
#            this_datagroup.MyKeyDict[key]##

#            return_string += key
#            return_string += " in context: "
#            return_string += alloform.Context
            
#            return_list.append(return_string) 
#        return return_list

    def prose_statement(self):
        alloform_dict=dict()
        alloform_list=list()
        elsewhere_case=None
        for alloform in self.Alloforms:
            print ("G",   alloform.Form, alloform.Context)
            key = alloform.Form
            if key not in alloform_dict:
                alloform_dict[key] = list()
            alloform_dict[key].append(alloform)
            if alloform.Context == "NULL":
                elsewherecase_form = alloform.Form
        number_of_alloforms= len(alloform_dict)

        for item in alloform_dict:
            temp_alloform = CAlloform(item, "", 0)
            alloform_list.append(alloform_dict[item])
            print ("W", item, alloform_dict[item])
            for subitem in item:
                temp_alloform.Context += " "+subitem.Context


        return_string = ""
        for alloform_no in range(number_of_alloforms):
            thisreportline = CReportLine()

            #alloform_list[alloform_no] is a  list of alloforms, all with the same Key
            key = alloform_list[alloform_no][0].Key # take the Key from the first one, because they are all the same

            context_list = list()
            for n in range(len(alloform_list[alloform_no])):

                context_list.append(alloform_list[alloform_no].context)  
            return_string += key + ":".join(context_list)    
        return return_string            

class CAlloform:
    def __init__(self,form, context, stemcount):
        self.Form = form
        self.Context = context
        self.StemCount = stemcount

class CProseReportLine:
    def __init__(self):
        self.MyList = list()
        self.MyLastItem = None

    def MakeReport(self):
        returnstring="hello!"
        for item in self.MyList:
            returnstring += item.MyHead
            for item2 in self.MyTail:
                returnstring += " " + item2
        if self.MyLastItem:
            returnstring += item.MyHead
            for item2 in self.MyTail:
                returnstring += " " + item2  
        return returnstring         


class CReportLineItem:
    def __init__(self):        
        self.MyHead = NULL
        self.MyTail = NULL

class CDataGroup:
    def __init__(self, type,count):
        self.Type = type
        self.MyKeyDict = dict()
        self.Count = count


    def display(self):
        colwidth1 = 20
        colwidth2 = 40
        countstring = str(self.Count)
        returnstring = countstring + " "*(4-len(countstring))
        string1 = ""
        string2 =""

        ItemList = list(self.MyKeyDict.keys())
        #if there is a word-finally, put it in last place


        for i in range(len(ItemList)):
            phone = ItemList[i]
            if "\#" in self.MyKeyDict[phone]:
                #word final phoneme
                word_final_phone = ItemList[i]
                del ItemList[i]
                ItemList.append(word_final_phone)
        #if there is a "NIL", then put it in first place.
        for i in range(len(ItemList)):
            phone=ItemList[i]
            if phone== "nil":
                del ItemList[i]
                ItemList.insert(0,"nil")



        if self.Type == "KeyAndList":
            for key in ItemList:
                NULL_flag = False
                string1 = "[" + key + "]" 
                string2 = ""
                returnstring += string1 + " "*(colwidth1-len(string1))
               
                FirstItemFlag= True
                for item in self.MyKeyDict[key]:
                    if item == "NULL":
                        NULL_flag = True
                        continue
                    if FirstItemFlag:
                        string2 += "before " 
                        FirstItemFlag = False
                    string2 += "/"+item + "/ "
                if NULL_flag:
                    if FirstItemFlag == False:
                        string2 += "and word-finally."
                    else:
                        string2 += "word-finally."
                returnstring += string2 + " "*(colwidth2- len(string2))

                     
             
        return returnstring
