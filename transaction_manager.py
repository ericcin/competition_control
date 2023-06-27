"""
Module Name: transaction_manager
Author: Equipe 3
Purpose: Gerenciador de transações.
Created: 2023-06-19
"""
import re
import pprint

from settings import debug_message, init_logger, inspect_type
from lock_manager import LockManager

from typing import Dict, List

logger = init_logger(__name__)

class Query:
    def __init__(self, query_string: str, parent_transaction: int, reference_lock_manager: LockManager) -> None:
        # debug_message(
        #     f"""Query: __init__:
        #         query_string = {query_string}
        #         parent_transaction = {parent_transaction}
        #         inspect_type(reference_lock_manager) = {inspect_type(reference_lock_manager)}
        #         reference_lock_manager = {reference_lock_manager}
        #     """
        # )
        if query_string.startswith("READ(") and query_string.endswith(")"):
            self.operation = "READ"
            self.required_lock = "S"
            self.variable = query_string[5:-1]
        elif query_string.startswith("WRITE(") and query_string.endswith(")"):
            self.operation = "WRITE"
            self.required_lock = "E"
            self.variable = query_string[6:-1]
        else:
            self.operation = "NO-OP"
            self.required_lock = "N"
            self.variable = None
        self.query_string = query_string
        self.query_status = {"result": "READY", "data_string": ""}
        self.transaction = parent_transaction
        self.lock_manager = reference_lock_manager
    
    def get_query_string(self) -> str:
        return self.query_string    

    def get_operation(self) -> str:
        return self.operation

    def get_variable(self) -> str:
        return self.variable

    def get_status(self) -> str:
        # debug_message(
        #     f"""Query: get_status (exit):
        #         inspect_type(self.query_status) = {inspect_type(self.query_status)}
        #         self.query_status = {self.query_status}
        #     """
        # )
        return self.query_status["result"]

    def get_lock(self) -> str:
        # debug_message(
        #     f"""Query: get_lock (exit):
        #         inspect_type(self.query_status) = {inspect_type(self.query_status)}
        #         self.query_status = {self.query_status}
        #     """
        # )
        return self.query_status["data_string"]

    def acquire_lock(self) -> str:
        # debug_message(
        #     f"""Query: acquire_lock:
        #      inspect_type(self.transaction) = {inspect_type(self.transaction)}
        #         self.transaction = {self.transaction}
        #         inspect_type(self.operation) = {inspect_type(self.operation)}
        #         self.operation = {self.operation}
        #         inspect_type(self.variable) = {inspect_type(self.variable)}
        #         self.variable = {self.variable}
        #     """
        # )
        # available_lock = self.transaction.has_lock(self.variable)
        if self.operation == "READ":
            self.query_status = self.lock_manager.acquire_shared_lock(self.variable, self.transaction)
        elif self.operation == "WRITE":
            self.query_status = self.lock_manager.acquire_exclusive_lock(self.variable, self.transaction)
        elif self.operation == "NO-OP":
            self.query_status = {"result": "SUCCESS", "data_string": "('N', '')"}
        else:
            self.query_status = {"result": "UNKNOWN STATE", "data_string": "('S', '')"}
        # debug_message(
        #     f"""Query: acquire_lock (exit):
        #         inspect_type(self.query_status) = {inspect_type(self.query_status)}
        #     """
        # )
        return self.query_status

    def release_lock(self) -> str:
        self.query_status["result"] = "LOCK RELEASED"
        return self.lock_manager.release_lock(self.variable, self.transaction)


class Transaction:
    def __init__(self, numeric_id: int, queries: str, reference_lock_manager: LockManager) -> None:
        # debug_message(
        #     f"""Transaction: __init__:
        #         inspect_type(queries) = {inspect_type(queries)}
        #         queries = {queries}
        #     """
        # )
        self.id = numeric_id
        self.transaction_string = queries
        queries = queries.strip().strip('[]').replace("\r\n", "\n")
        self.query_strings = [item.strip() for item in re.split(r',|;|\n', queries) if item and not item.startswith(("--", "# "))]
        self.queries = [Query(query_string, numeric_id, reference_lock_manager) for query_string in self.query_strings]
        self.lock_manager = reference_lock_manager
        self.next_query = 0
        self.phase = "Expanding"
        self.transaction_status = "READY"

    def get_id(self) -> int:
        return self.id

    def get_transaction_string(self) -> str:
        return f"{self.id}: {self.transaction_string}"

    def get_next_query(self) -> int:
        return self.next_query

    def get_query_strings(self) -> List[str]:
        return self.query_strings
    
    def get_phase(self) -> str:
        return self.phase

    def get_status(self) -> str:
        return self.transaction_status

    def get_locks(self) -> List[str]:
        return self.lock_manager.list_transaction_locks(self.id)

    def has_lock(self, data_item):
        return self.lock_manager.transaction_has_lock(data_item, self.id)

    def has_waiting_query(self) -> bool:
        for query in self.queries:
            if query.get_status() == "WAIT":
                return True
        return False


    def step_into(self) -> str:
        debug_message("Transaction: step_into")
        debug_message(
            f"""Transaction: step_into:
                inspect_type(self.phase) = {inspect_type(self.phase)}
                inspect_type(self.transaction_status) = {inspect_type(self.transaction_status)}
                inspect_type(self.transaction_string) = {inspect_type(self.transaction_string)}
                inspect_type(self.next_query) = {inspect_type(self.next_query)}
            """
        )
        situation = "INVALID STATUS"
        if self.transaction_status not in ["COMMITED", "KILLED", "DEAD"]:
            if self.transaction_status == "READY":
                self.transaction_status = "EXECUTING"

            if self.phase == "Expanding":
                pending_queries = [query for query in self.queries if query.get_status() in ["READY", "WAIT"]]
                if len(pending_queries) == 0:
                    self.phase = "Shrinking"
                    self.transaction_status = "RELEASING LOCKS"
                else:
                    attempt_lock = self.queries[self.next_query].acquire_lock()
                    pprint.pprint(attempt_lock)
                    detailed_result = attempt_lock["data_string"]
                    if attempt_lock["result"] == "SUCCESS":
                        self.next_query = self.next_query + 1
                    if attempt_lock["result"] == "WAIT":
                        self.status = f"WAITING FOR {detailed_result}"
                    else:
                        self.status = detailed_result
                # else:
                #     for query in pending_queries:
                #         query.acquire_lock()
                #     situation = "EXECUTING"


            elif self.phase == "Shrinking":
                # active_queries = [query for query in self.queries if query.get_status() in ["READ", "WRITE"]]
                # if len(active_queries) == 0:
                #     self.transaction_status = "COMMITED"
                #     situation = self.transaction_status
                # else:
                    # for query in active_queries:
                    #     query.release_lock()
                self.lock_manager.remove_transaction_locks(self.id)
        
            if self.has_waiting_query():
                situation = "WAITING"
        else:
            situation = self.transaction_status
        debug_message(
            f"""Transaction: step_into (exit):
                inspect_type(self.transaction_status) = {inspect_type(self.transaction_status)}
                inspect_type(self.phase) = {inspect_type(self.phase)}
                inspect_type(situation) = {inspect_type(situation)}
            """
        )
        return situation

    def be_murdered(self) -> str:
        self.transaction_status = "KILLED"
        self.lock_manager.remove_transaction_locks(self.id)
        return self.transaction_status

    def die(self) -> str:
        self.transaction_status = "DEAD"
        self.lock_manager.remove_transaction_locks(self.id)
        return self.transaction_status

class TransactionManager:
    def __init__(self, reference_lock_manager: LockManager, transactionList: List[str] = None) -> None:
        # debug_message(
        #     f"""TransactionManager: __init__:
        #         inspect_type(reference_lock_manager) = {inspect_type(reference_lock_manager)}
        #         reference_lock_manager = {reference_lock_manager}
        #         inspect_type(transactionList) = {inspect_type(transactionList)}
        #         transactionList = {transactionList}
        #     """
        # )
        if transactionList is None:
            transactionList = [
                "[READ(Users);READ(Products);WRITE(Orders);]"
                ,"[READ(Users);WRITE(Users);WRITE(Orders);]"
                # ,"[WRITE(Orders);READ(Orders)]"
                ,"[READ(Orders);READ(Orders)]"
            ]
            # transactionList = [
            #     "READ(Users)"
            #     ,"WRITE(Users)"
            #     ,"READ(Orders)"
            # ]

        self.lock_manager = reference_lock_manager
        self.transactionList: List[Transaction] = [Transaction(i, transaction_string, reference_lock_manager) for i, transaction_string in enumerate(transactionList, start=1)]

    def get_last_id(self) -> int:
        return max(transaction.get_id() for transaction in self.transactionList)

    def add_transaction(self, transaction_string: str) -> None:
        self.transactionList.append(Transaction(self.get_last_id()+1, transaction_string, self.lock_manager))
        return self.list_transactions()

    def remove_transaction_by_id(self, transaction: Transaction) -> None:
        self.transactionList.remove(transaction)

    def remove_transaction_by_queries(self, transaction: Transaction) -> None:
        self.transactionList.remove(transaction)

    def list_transactions(self) -> List[Dict[str, str]]:
        debug_message("TransactionManager: list_transactions")
        transaction_list = [
            {
                'id': str(transaction.get_id()),
                'commands': transaction.get_query_strings(),
                'next_query': transaction.get_next_query(),
                'phase': transaction.get_phase(),
                'status': transaction.get_status(),
                'locks': transaction.get_locks(),
                'formatted_locks': self.list_locks()
            }
            for transaction in self.transactionList
        ]
        # debug_message(
        #     f"""TransactionManager: list_transactions (exit):
        #         inspect_type(transaction_list) = {inspect_type(transaction_list)}
        #     """
        # )
        return transaction_list


    def list_locks(self) -> List[Dict[str, str]]:
        debug_message("TransactionManager: list_locks")
        data_items: List[str] = self.lock_manager.list_data_items()
        transactions: List[str] = [transaction.get_id() for transaction in self.transactionList]
        locksTable: List[Dict[str, str]] = []
        for data_item in data_items:
            rowDict: Dict[str, str] = {}
            rowDict["Item de Dados"] = data_item
            for transaction in transactions:
                rowDict[transaction] = self.lock_manager.get_lock_status(data_item, transaction)
            locksTable.append(rowDict)
        # debug_message(
        #     f"""TransactionManager: list_locks (exit):
        #         inspect_type(locksTable) = {inspect_type(locksTable)},
        #     """
        # )
        pprint.pprint(locksTable)
        return locksTable

    def step_into(self) -> List[Dict[str, str]]:
        debug_message("TransactionManager: step_into")
        [transaction.step_into() for transaction in self.transactionList]
        transaction_data = self.list_transactions()
        print("transaction_data: ")
        pprint.pprint(transaction_data)
        return transaction_data