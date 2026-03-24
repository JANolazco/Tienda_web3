create table products (
  id bigint primary key generated always as identity,
  name text not null,
  description text,
  price numeric(10, 2) not null,
  stock int not null
);

create table sales (
  id bigint primary key generated always as identity,
  product_id bigint references products (id),
  quantity int not null,
  total_price numeric(10, 2) not null,
  sale_date timestamp with time zone default now()
);

create table cash_register (
  id bigint primary key generated always as identity,
  opening_balance numeric(10, 2) not null,
  closing_balance numeric(10, 2),
  date timestamp with time zone default now()
);