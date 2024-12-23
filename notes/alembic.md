# Different alembic commands

## Create Table

```python

op.create_table(
    'users',
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('name', sa.String(50), nullable=False),
    sa.Column('email', sa.String(100), unique=True)
)
```

## Create Foreign Key

```python

op.create_table(
    'users',
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('name', sa.String(50), nullable=False),
    sa.Column('email', sa.String(100), unique=True)
)
```

## Create Index

```python

op.create_index(
    'idx_name',         # index name
    'table_name',       # table to index
    ['column_name'],    # columns to index
    unique=False        # uniqueness constraint
)
```

## Add Column

```python

op.add_column(
    'table_name',
    sa.Column('column_name', sa.String(50))
)
```

## Drop Operation

```python

# Drop table
op.drop_table('table_name')

# Drop column
op.drop_column('table_name', 'column_name')

# Drop foreign key
op.drop_constraint('fk_name', 'table_name')

# Drop index
op.drop_index('idx_name', 'table_name')
```

## Alter column

```python

op.alter_column(
    'table_name',
    'column_name',
    new_column_name='new_name',
    type_=sa.String(100),
    nullable=False
)
```

## Create Unique Contraints

```python

op.create_unique_constraint(
    'constraint_name',
    'table_name',
    ['column_1', 'column_2']
)
```
