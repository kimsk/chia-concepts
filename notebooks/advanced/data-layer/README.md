# Chia DataLayer


## Data Tables (Key/Value Data Stores)
- Each data store of data is represented by a singleton coin.

- The table singleton stores:
    - An immutable identifier
    - SHA-256 of data store in that table (Merkle Tree)
    - A list of users with write access 

- The table singleton Chialisp

### Relational Data
- Each row is represented by a data store (singleton coin)

> karlkim: From what I read, Data Layer is supporting relational data, but I only see api interacts with keys/values (only hex data) right now.

> rigidity: It's still stored as key-value
The key is the table name and primary key columns
The value is the rest of the columns
So it sort of emulates a relational database

> karlkim: From this code, https://github.com/Chia-Network/climate-warehouse/blob/main/src/models/organizations/organizations.model.js#L75, it looks like each row on the table is represented by DataStore and each key is a column. So each row will have associated singleton coin, right?
I think I see the pattern. We can store bothb relational or key/value data. This is cool.

## Validator Nodes
- Each validator node operator has the option to "subscribe" to DataLayer tables.
- Whenever the singleton is updated, all of the nodes that subscribe to that table will get the updated data while using updated hash to verify updated data.
- Efficient P2P network
- If at any point there are no nodes subscribing to the data for a data table singleton, that data will be lost.

- TBA, restricted read access
- TBA, large binary data

## Relational Data
- Unique hash of data as PK
- No duplicate rows
- FK

### Querying
- Fetch one by the row pk
- Fetch all rows
- Query for the inserted/deleted rows associated by commint number
- Query to get the current commit number

## Data Analytics & DataLayer API
- read-only data access API
- write data access API
- notification when a DataLayer table has changed
- ETL
- 2-party commits
- Transaction (or Offer files) for correspondint database updates to data tables owned by two parties.
    - Alice and Bob agree to update their own tables simultaneously.







