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


CREATE TABLE tafseer_details (
    id bigint unsigned not null auto_increment,
    author varchar(100) not null,
    name varchar(100) not null,
    description text,
    primary key tafseer_detail_id (id)
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

create table editions (
    id bigint unsigned auto_increment,
    identifier varchar(50) not null,           
    edition_name varchar(255) not null,                       
    english_name varchar(255),
    lang char(2) not null,                        
    type_ Enum('translation','tafsir') not null,
    direction Enum('ltr','rtl'),
    tafseer_detail_id bigint unsigned,       
    primary key edition_id (id),
    unique key edition_identifier (identifier),
    constraint tafseer_edition foreign key (tafseer_detail_id) references tafseer_details(id) on delete set null on update cascade
);

create table verse_translations (
    id bigint unsigned auto_increment not null,
    verse_id bigint unsigned not null,
    edition_id bigint unsigned not null, 
    translation_text longtext not null,
    primary key verse_translation_id (id), 
    unique key verse_edition (verse_id, edition_id),
    constraint translation_verse_id foreign key (verse_id) references verse(id) on delete cascade on update cascade,
    constraint traslation_edition_id foreign key (edition_id) references editions(id) on delete cascade on update cascade
);

create table verse_tafsirs (
    id bigint unsigned auto_increment not null,
    verse_id bigint unsigned not null,
    edition_id bigint unsigned not null,     
    tafseer_text longtext not null,
    primary key verse_tafseer_id (id), 
    constraint tafseer_verse_id foreign key (verse_id) references verse(id) on delete cascade on update cascade,
    constraint tafseer_edition_id foreign key (edition_id) references editions(id) on delete cascade on update cascade
);

show tables