import unittest

class test_api(TestCase):
    groupOfColumns1 = {}
    groupOfColumns2 = {}
    groupOfColumns3 = {}
    
    
    
    def setUp(self):
        pass

    def test_00_init(self):
        ans1 = self.__transformGroupInList(groupOfColumns1)
        ans2 = self.__transformGroupInList(groupOfColumns2)
        ans3 = self.__transformGroupInList(groupOfColumns3)
        
        self.assertTrue(ans1, "")
            
        self.assertEqual(n_app_tasks,
               len(pbclient.get_tasks(pb_app[0].id, sys.maxint)),
                    "Error duplicated tasks")


        """
     Transform group of columns in one list of consistent
     columns.
    """
    def __transformGroupInList(self, groupOfColumns):
        sortedGroupOfColumns = sorted(groupOfColumns, key=itemgetter(1))
        print "sortedGroupOfColumns"
        print sortedGroupOfColumns
        
        listOfColumns = []
        
        ptr1 = None
        ptr2 = None
        #mapOfContinuousCols = {}
        tmpCols = [sortedGroupOfColumns[0]]
        for i in range(1, len(sortedGroupOfColumns)-1):   # find other columns to join
            ptr1 = sortedGroupOfColumns[i]
            ptr2 = sortedGroupOfColumns[i+1]
            
            if (ptr2[1] - ptr1[3] <= 0): # is a continuous column
                #idGroup = self.__identifyGroupIdInY(mapOfContinuousCols, ptr1)
                
                #if(mapOfContinuousCols.has_key(idGroup)):
                #    mapOfContinuousCols[idGroup].append(ptr1)
                tmpCols.append(ptr1)
                if(i+1 == len(sortedGroupOfColumns)-1):
                    tmpCols.append(ptr2)
                #else:
                #    mapOfContinuousCols[idGroup] = [ptr1]
            else:
                #mapOfContinuousCols[idGroup] = [ptr1]
                listOfColumns.append([tmpCols[0][0],
                                      tmpCols[0][1],
                                      tmpCols[0][2],
                                      tmpCols[-1][3]])
                tmpCols = [ptr2]
                print "listOfColumns"
                print listOfColumns
       
      
        listOfColumns.append([tmpCols[0][0],
                             tmpCols[0][1],
                             tmpCols[0][2],
                             tmpCols[-1][3]])
            
       #     print "mapOfContinuousCols"
       #     print mapOfContinuousCols
            
        #if(ptr2 == sortedGroupOfColumns[-1]):
        #    idGroup = self.__identifyGroupIdInY(mapOfContinuousCols, ptr2)
        #    
        #    if(mapOfContinuousCols.has_key(idGroup)):
        #        mapOfContinuousCols[idGroup].append(ptr2)
        #    else:
        #        mapOfContinuousCols[idGroup] = [ptr2]
       # 
        #for i in range(0,len(mapOfContinuousCols.values())):
        #   list = mapOfContinuousCols.values()[i]
        #    listOfColumns.append([list[0][0],
        #                          list[0][1],
        #                          list[0][2],
         #                         list[-1][3]])
        
        #listCols.append()
                
        print "listOfColumns"
        print listOfColumns
        
        return listOfColumns

def suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(test_api)
    return suite
