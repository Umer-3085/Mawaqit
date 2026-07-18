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
    name_arabic varchar(100) not null,
    english_name varchar(100) not null,
    english_name_translation varchar(100) not null,
    relevation_type Enum('Meccan','Medinan') not null,
    primary key surah_no (surah_number),
    unique key surah_names (name_arabic)
);

create table verse (
	id bigint unsigned not null auto_increment,
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
    primary key verse_identifier (id),
    constraint foreign_surah_no foreign key ( surah_number ) references surah ( surah_number ) on delete cascade on update cascade
);

CREATE TABLE translation_tafseer_details (
    id bigint unsigned not null auto_increment,
    identifier varchar(50) not null,
    english_name varchar(255),
    lang char(2) not null,     
    type_ Enum('translation','tafsir') not null,             
    author varchar(100) not null,
    direction Enum('ltr','rtl'),
    edition_name varchar(255) not null,
    description text,
    primary key tafseer_detail_id (id),
    unique key edition_identifier ( identifier ) 
);

create table verse_texts (
    id bigint unsigned not null auto_increment,
    verse_id bigint unsigned not null,
    detail_id bigint unsigned not null,
    text_type Enum('translation','tafsir') not null,
    text_content longtext not null,
    primary key verse_text_id (id),
    unique key verse_detail_type (verse_id, detail_id, text_type),
    constraint verse_identifier foreign key (verse_id) references verse (id) on delete cascade on update cascade,
    constraint verse_texts_identifier foreign key (detail_id) references translation_tafseer_details (id) on delete cascade on update cascade
);

show tables
