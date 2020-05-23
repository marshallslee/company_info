SELECT * FROM company_tag WHERE tag_group_id IN (
	SELECT tag_group_id FROM tag WHERE name="tag_2"
);
