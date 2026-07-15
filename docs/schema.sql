create database if not exists mawaqit;
use mawaqit;

create table admin (
    username varchar(100) not null,
    password_hash varchar(255) not null, 
    unique key admin_name (username)
);

create table category (
	id bigint unsigned not null auto_increment,
    title varchar(255) not null,
    primary key category_id (id),
    unique key category_title (title)
);

create table subcategory (
	id bigint unsigned not null auto_increment,
    title varchar(255) not null,
    category_id bigint unsigned not null,
    primary key subcategory_id (id),
    unique key subcategory_title (title),
    constraint foreign_category_id foreign key ( category_id ) references category ( id ) On delete cascade on update cascade
);

create table article_videos (
	id bigint unsigned not null auto_increment,
    title varchar(500) not null,
    detail longtext,
    category_id bigint unsigned not null,
    subcategory_id bigint unsigned,
    link varchar(1000),
    primary key articel_videos_id (id),
    constraint foreign_category_id_for_articel_videos foreign key ( category_id ) references category (id) ON DELETE RESTRICT ON UPDATE CASCADE,
    constraint foreign_subcategory_id foreign key ( subcategory_id ) references subcategory (id) ON DELETE SET NULL ON UPDATE CASCADE
);

create table surah (
	surah_number tinyint unsigned not null,
    total_ayat smallint unsigned not null,
    arabic text,
    primary key surah_no (surah_number)
);

create table verse (
	verse_number int unsigned not null,
    arabic text,
    surah_number tinyint unsigned not null,
    primary key verse_no (verse_number),
    constraint foreign_surah_no foreign key ( surah_number ) references surah ( surah_number ) on delete cascade on update cascade
);

create table tafseer_detail (
	id bigint unsigned not null auto_increment,
    author varchar(100) not null,
    name varchar(100) not null,
    description text,
    primary key tafseer_detail_id ( id )
);

create table translation_tafseer (
	id bigint unsigned not null auto_increment,
    translation longtext,
    tafseer longtext,
    lang varchar(10) not null,
    surah_no tinyint unsigned not null,
    verse_no int unsigned not null,
    tafseer_id bigint unsigned not null,
    primary key translation_tafseer_id ( id ),
    constraint foreign_surah_no_for_detail foreign key ( surah_no ) references surah ( surah_number ) on delete cascade on update cascade,
    constraint foreign_verse_no foreign key ( verse_no ) references verse ( verse_number ) on delete cascade on update cascade,
    constraint foreign_tafseer_id foreign key ( tafseer_id ) references tafseer_detail ( id ) on delete cascade on update cascade
);    