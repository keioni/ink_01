-- Test SQL reading and coverting system
-- used in pytest (tests/test_database.py)

--


-- format does not match correctly,
-- but there are the same
        create table tokens (
    rowid integer auto_increment,
                                token bigint,
user_id integer,
        ctime datetime not null,
                        primary key (token),
)
;

-- inline comment
create table users ( -- comment
    rowid integer auto_increment,       -- comment comment
    token bigint,--comment
    user_id integer,
    ctime datetime not null,
    primary key (token),
)
;

create table boxes (
    box_id integer auto_increment,
    user_id integer,
    box_title varchar(32) not null,
    ctime datetime,
    mtime datetime,
    primary key (box_id),
    index index_user (user_id),
);

-- select * from cards where user_id=$UID
-- select * from cards where user_id=$UID and box_id=$BID
create table cards (
    card_id integer auto_increment,
    box_id integer,
    user_id integer,
    card_title varchar(32) not null,
    ctime datetime,
    mtime datetime,
    recent_records char(340),
    primary key (card_id),
    index index_user_box (user_id, box_id),
)
;

-- select record from records where card_id=$CID
create table records (
    rowid integer auto_increment,
    card_id integer,
    record char(16),
    primary key (rowid),
    index index_card (card_id),
)
;
