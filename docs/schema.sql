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
    description text,
    primary key category_id (id),
    unique key category_title (title)
);

create table subcategory (
	id bigint unsigned not null auto_increment,
    title varchar(255) not null,
    category_id bigint unsigned not null,
    description text,
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
    name_arabic varchar(100) not null,
    english_name varchar(100) not null,
    english_name_translation varchar(100) not null,
    relevation_type Enum('Meccan','Medinan') not null,
    primary key surah_no (surah_number),
    unique key surah_names (name_arabic)
);

create table verse (
	number_in_surah int unsigned not null,
    arabic text,
    surah_number tinyint unsigned not null,
    global_number int unsigned unique not null,
    juz tinyint unsigned,
    manzil tinyint unsigned,
    page_no smallint unsigned,
    ruku smallint unsigned,
    hizb_quarter tinyint unsigned,
    sajda boolean default false,
    primary key verse_identifier (surah_number,number_in_surah),
    constraint foreign_surah_no foreign key ( surah_number ) references surah ( surah_number ) on delete cascade on update cascade
);

create table translation_tafseer_details (
    id bigint unsigned not null auto_increment,
    title varchar(255) not null,
    lang char(2) not null,     
    author varchar(100) not null,
    direction Enum('ltr','rtl'),
    description text,
    primary key tafseer_detail_id (id),
    unique key translation_tafseer_title ( title ) 
);

create table verse_texts (
	surah_number tinyint unsigned not null,
    verse_number int unsigned not null,
    detail_id bigint unsigned not null,
    verse_translation longtext not null,
    verse_tafseer longtext,
    primary key verse_text_id (surah_number,verse_number),
    constraint foreign_surah_and_verse_no_for_text foreign key ( surah_number,verse_number ) references verse ( surah_number,number_in_surah ) on delete cascade on update cascade,
    constraint verse_texts_identifier foreign key (detail_id) references translation_tafseer_details (id) on delete cascade on update cascade
);

show tables
drop table verse_texts;
drop table verse;
drop table surah;
drop table translation_tafseer_details;
drop table article_videos;
drop table admin,subcategory;
drop table category;