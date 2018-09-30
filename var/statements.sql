-- INK system SQL statements.
-- Because these statement use Python string format,
-- you cannot use this file by DBMS client program

-- [get boxes]
select * from boxes where user_id={uid}

-- [get cards]
select * from cards where user_id={uid}

-- [get cards using box id]
select * from cards where user_id={uid} and box_id={box_id}

-- [get records]
select record from records where card_id={card_id}
