from collections import defaultdict
from dqn.dialogue_config import no_query_keys, usersim_default_key
import copy


class DBQuery:
    """Queries the database for the state tracker."""

    def __init__(self, database):
        """
        The constructor for DBQuery.

        Parameters:
            database (dict): The database in the format dict(long: dict)
        """

        self.database = database
        # {frozenset: {string: int}} A dict of dicts
        self.cached_db_slot = defaultdict(dict)
        # {frozenset: {'#': {'slot': 'value'}}} A dict of dicts of dicts, a dict of DB sub-dicts
        self.cached_db = defaultdict(dict)
        self.no_query = no_query_keys
        self.match_key = usersim_default_key

    def fill_inform_slot(self, inform_slot_to_fill, current_inform_slots):
        """
        Given the current informs/constraints fill the informs that need to be filled with values from the database.

        Searches through the database to fill the inform slots with PLACEHOLDER with values that work given the current
        constraints of the current episode.

        Parameters:
            inform_slot_to_fill (dict): Inform slots to fill with values
            current_inform_slots (dict): Current inform slots with values from the StateTracker

        Returns:
            dict: inform_slot_to_fill filled with values
        """

        # For this simple system only one inform slot should ever passed in
        assert len(inform_slot_to_fill) == 1

        key = list(inform_slot_to_fill.keys())[0]

        # This removes the inform we want to fill from the current informs if it is present in the current informs
        # so it can be re-queried
        current_informs = copy.deepcopy(current_inform_slots)
        # current_informs.pop(key, None)

        # db_results is a dict of dict in the same exact format as the db, it is just a subset of the db
        db_results = self.get_db_results(current_informs)
        print("current informs: {}".format(current_informs))

        filled_inform = {}
        values_dict = self._count_slot_values(key, db_results)
        # print("key: {}".format(key))
        print("db results: {}".format(db_results))

        if values_dict:
            # Get key with max value (ie slot value with highest count of available results)
            filled_inform[key] = max(values_dict, key=values_dict.get)
        else:
            filled_inform[key] = 'no match available'

        return filled_inform

    def _count_slot_values(self, key, db_subdict):
        """
        Return a dict of the different values and occurrences of each, given a key, from a sub-dict of database

        Parameters:
            key (string): The key to be counted
            db_subdict (dict): A sub-dict of the database

        Returns:
            dict: The values and their occurrences given the key
        """

        slot_values = defaultdict(int)  # init to 0
        # print(slot_values)
        for id in db_subdict.keys():
            current_option_dict = db_subdict[id]
            # If there is a match
            if key in current_option_dict.keys():
                slot_value = current_option_dict[key]
                # print(slot_value)
                if any(isinstance(i,list) for i in slot_value):
                  slot_value = [value for sub_list in slot_value for value in sub_list]

          
                tp_slot_value = tuple(slot_value)
                # print(type(tp_slot_value))
                # This will add 1 to 0 if this is the first time this value has been encountered, or it will add 1
                # to whatever was already in there
                slot_values[tp_slot_value] += 1
        return slot_values

    def check_match_sublist_and_substring(self,list_children,list_parent):
        # print("match sublist")
        count_match=0
        for children_value in list_children:
            for parent_value in list_parent:
                if children_value in parent_value:
                    count_match+=1
                    break
        if count_match==len(list_children):
            # print("match sublist")
            return True
        return False
            



    def get_db_results(self, constraints):
        """
        Get all items in the database that fit the current constraints.

        Looks at each item in the database and if its slots contain all constraints and their values match then the item
        is added to the return dict.

        Parameters:
            constraints (dict): The current informs

        Returns:
            dict: The available items in the database
        """

        # Filter non-queryable items and keys with the value 'anything' since those are inconsequential to the constraints
        new_constraints = {k: v for k, v in constraints.items() if k not in self.no_query and v is not 'anything'}
        # print('>'*50)
        # print(constraints)
        # print('>'*50)
        tuple_new_constraint=copy.deepcopy(new_constraints)
        # print(tuple_new_constraint)
        inform_items ={k:tuple(v) for k,v in tuple_new_constraint.items()}.items()
        inform_items = frozenset(inform_items)
 
        # inform_items = frozenset(new_constraints.items())
        cache_return = self.cached_db[inform_items]
 
        if cache_return == None:
            # If it is none then no matches fit with the constraints so return an empty dict
            return {}
        # if it isnt empty then return what it is
        if cache_return:
            return cache_return
        # else continue on

        available_options = {}
        # results=[]
        i=0
        for data in self.database:
            check_match=True
            for constraint_key in list(new_constraints.keys()):
                if not self.check_match_sublist_and_substring(new_constraints[constraint_key],data[constraint_key]): #check not sublist and substring
                    check_match=False
            if check_match:
                # print("have match result")
                # results.append(data)
                available_options.update({str(i):data})
                self.cached_db[inform_items].update({str(i): data})
            i+=1

        

        # for result in results:
        #     available_options.update({str(result['_id']):result})
        #     self.cached_db[inform_items].update({str(result['_id']): result})

        if not available_options:
          self.cached_db[inform_items] = None

        #   print("no match: ")
          # print(new_constraints)

 
        return available_options

    def get_db_results_for_slots(self, current_informs):
        """
        Counts occurrences of each current inform slot (key and value) in the database items.

        For each item in the database and each current inform slot if that slot is in the database item (matches key
        and value) then increment the count for that key by 1.

        Parameters:
            current_informs (dict): The current informs/constraints

        Returns:
            dict: Each key in current_informs with the count of the number of matches for that key
        """

        tuple_current_informs=copy.deepcopy(current_informs)
        # print(tuple_current_informs)
        inform_items ={k:tuple(v) for k,v in tuple_current_informs.items()}.items()
        inform_items = frozenset(inform_items)
        # # A dict of the inform keys and their counts as stored (or not stored) in the cached_db_slot
        cache_return = self.cached_db_slot[inform_items]
        # temp_current_informs=copy.deepcopy(current_informs)
        if cache_return:
            return cache_return
 
        # If it made it down here then a new query was made and it must add it to cached_db_slot and return it
        # Init all key values with 0
        db_results = {key: 0 for key in current_informs.keys()}
        db_results['matching_all_constraints'] = 0



        for data in self.database:
            all_slots_match = True
            for CI_key, CI_value in current_informs.items():
                # Skip if a no query item and all_slots_match stays true
                if CI_key in self.no_query:
                    continue
                # If anything all_slots_match stays true AND the specific key slot gets a +1
                if CI_value == 'anything':
                    db_results[CI_key] += 1
                    continue
                if CI_key in list(data.keys()):
                    # print("-----------------CI_value")
                    # print(type(CI_value))
                    # print("-----------------data[CI_key]")
                    # print(type(data[CI_key]))
                    if self.check_match_sublist_and_substring(CI_value,data[CI_key]):
                        db_results[CI_key] += 1
                    else:
                        all_slots_match = False
                else:
                    all_slots_match = False
            if all_slots_match: db_results['matching_all_constraints'] += 1



        # update cache (set the empty dict)
        self.cached_db_slot[inform_items].update(db_results)
        assert self.cached_db_slot[inform_items] == db_results
        return db_results
