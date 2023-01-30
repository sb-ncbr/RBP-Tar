DROP INDEX IF EXISTS chromosome_idx;
DROP INDEX IF EXISTS start_idx;
DROP INDEX IF EXISTS end_idx;
DROP INDEX IF EXISTS strand_idx;
DROP INDEX IF EXISTS  protein_name_idx;

CREATE INDEX chromosome_idx ON genes(chromosome);
CREATE INDEX start_idx ON genes(start);
CREATE INDEX end_idx ON genes(end);
CREATE INDEX strand_idx ON genes(strand);
CREATE INDEX protein_name_idx ON genes(protein_name);
