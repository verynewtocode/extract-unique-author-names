-- Which GitHub organisations own the most packages in the dataset?
-- Query the owner table only and group by ownership.organization where non-null.

SELECT
    organization,
    COUNT(*) AS package_count
FROM ssc.dim_owner
WHERE organization IS NOT NULL
GROUP BY organization
ORDER BY package_count DESC, organization;
