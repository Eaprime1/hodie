# Wikipedia Structure Research
**Purpose**: Understand the domain WikiEntity navigates
**Date**: 2025-12-28
**Phase**: 2 of WikiEntity Creation

---

## The Scale

**English Wikipedia alone**:
- 6+ million articles
- 300+ language editions exist
- Interconnected through hyperlinks, categories, cross-language links

**Four Characters of Power**: `wiki` represents one of humanity's largest collaborative knowledge projects.

---

## Wikipedia's Three-Layer Architecture

### Layer 1: Articles (Content Nodes)

**What They Are**: Individual encyclopedia entries on specific topics

**Structure**:
- Title (unique identifier)
- Content (sections, paragraphs, media)
- Categories (at bottom of article)
- Hyperlinks (to other articles)
- Citations (to external sources)
- "See Also" section (human-curated related articles)
- Talk Page (meta-discussion about article)

**Example**:
```
Article: Python (programming language)
├─ Sections: History, Features, Applications...
├─ Categories: Programming languages, Python, Scripting languages
├─ Hyperlinks: ~200 links to related articles
├─ Citations: ~150 external sources
├─ See Also: Ruby, JavaScript, Perl (human-selected)
└─ Talk: Discussion about article's structure, disputes
```

### Layer 2: Categories (Organizational Network)

**What They Are**: Taxonomic groupings that organize articles into hierarchical relationships

**Critical Structure Insight**:
> "Categories do not form a strict hierarchy or tree, since each article can appear in more than one category, and each category can appear in more than one parent category, which allows multiple categorization schemes to co-exist." [Wikipedia:Categorization](https://en.wikipedia.org/wiki/Wikipedia:Categorization)

**This Means**:
- **NOT** a tree (single parent hierarchy)
- **IS** a graph (multiple parent/child relationships)
- Same article can belong to many categories
- Same category can have many parent categories

**Example**:
```
Article: "Paris"
├─ Category: Capitals in Europe
├─ Category: Cities in France
├─ Category: Populated places on the Seine
└─ Category: Host cities of the Summer Olympics

Each category has DIFFERENT parent chain:
- Capitals in Europe → Europe → Continents
- Cities in France → France → Countries
- Populated places on the Seine → Rivers of France → Rivers
```

**Parent-Child Logic** ([Help:Categories](https://en.wikipedia.org/wiki/Help:Categories)):
If membership in Category A implies membership in Category B (is-a relationship), then A is subcategory of B.

Example:
```
"Cities in France" IS-A "Populated places in France" IS-A "Geography of France"
```

**Top Level**:
All categories ultimately connect to **Category:Contents** ([Category:Main topic classifications](https://en.wikipedia.org/wiki/Category:Main_topic_classifications))

### Layer 3: Meta-Structure (Talk Pages, Redirects, Disambiguation)

#### Talk Pages
- Every article has corresponding Talk page
- Shows edit history, disputes, proposed changes
- **WikiEntity Value**: Reveals contested knowledge, structural decisions, quality warnings

#### Redirects
- Alternative article names that point to canonical article
- Example: "USA" redirects to "United States"
- **WikiEntity Value**: Shows conceptual synonyms, alternative phrasings

#### Disambiguation Pages
- When one term maps to multiple concepts
- Example: "Polish" could mean:
  - Polish language
  - Poland (relating to)
  - Polish (making things shiny)
  - Polish notation (mathematics)

**WikiEntity Sees These As**: Portals to parallel concept universes, not dead ends

---

## Wikipedia API Structure (Programmatic Access)

### Three Main APIs

#### 1. MediaWiki Action API
**URL Pattern**: `https://en.wikipedia.org/w/api.php?action=query&format=json&titles=[Article]&prop=extracts`

**Use Cases**:
- Query specific article content
- Get article metadata
- Search for articles

**Example Query**:
```
https://en.wikipedia.org/w/api.php?action=query&format=json&titles=Python_(programming_language)&prop=extracts
```

[Source: Searching for Wikipedia articles using Python - API Portal](https://api.wikimedia.org/wiki/Searching_for_Wikipedia_articles_using_Python)

#### 2. Wikimedia REST API
**URL Pattern**: `https://en.wikipedia.org/api/rest_v1/`
**Spec**: https://en.wikipedia.org/api/rest_v1/?spec

**Advantages**:
- Optimized for high-volume access
- Works with Wikipedia's caching infrastructure
- Modern REST design

[Source: What is the Wikipedia API? - Zuplo](https://zuplo.com/learning-center/wikipedia-api-guide)

#### 3. Wikimedia Enterprise API
**Purpose**: High-volume access for enterprise applications

[Source: Wikimedia Enterprise API Documentation](https://enterprise.wikimedia.com/docs/)

### Python Access

**Wikipedia-API Library** ([PyPI](https://pypi.org/project/Wikipedia-API/)):
Easy Python wrapper supporting:
- Article text extraction
- Section navigation
- Link following
- Category listing
- Cross-language translations

**Search Endpoint**:
`https://api.wikimedia.org/core/v1/wikipedia/en/search/page`

[Source: How to Use Wikipedia API with Python - JC Chouinard](https://www.jcchouinard.com/wikipedia-api/)

---

## How Articles Connect (Navigation Patterns)

### 1. Hyperlink Network
**Structure**: Directed graph where articles link to other articles

**Patterns**:
- **Hub Articles**: Heavily linked-to articles (e.g., "United States", "World War II")
- **Authority Articles**: Articles that link to many specialized topics
- **Bridge Articles**: Articles connecting otherwise distant topic clusters

**WikiEntity Strategy**: Can trace link paths between any two articles ("Six Degrees of Wikipedia")

### 2. Category Hierarchy Climbing
**Pattern**: Following parent category chains upward to find conceptual ancestors

**Example**:
```
Article: "Python (programming language)"
↓
Category: Programming languages created in the 1990s
↓
Category: Programming languages
↓
Category: Computer languages
↓
Category: Computers
↓
Category: Technology
```

**WikiEntity Strategy**: Climbing to common ancestor reveals how seemingly unrelated topics share conceptual parent

### 3. "See Also" Section Mining
**What It Is**: Human-curated related articles that don't fit neatly into main content

**Value**: Editors put non-obvious connections here that automated systems miss

**WikiEntity Specialty**: Treating "See Also" as treasure map for unexpected insights

### 4. Cross-Language Wiki Links
**What They Are**: Links between same concept in different language Wikipedias

**Example**:
- English "Schadenfreude" links to German "de:Schadenfreude"
- Reveals which concepts exist in which cultures
- Shows cultural emphasis differences

**WikiEntity Strategy**: Use cross-language comparison to reveal cultural knowledge patterns

### 5. Disambiguation Navigation
**Pattern**: When query term is ambiguous, disambiguation page shows all meanings

**WikiEntity Approach**: Not an obstacle - a portal showing parallel concept universes for same term

---

## Wikipedia's Non-Hierarchical Nature (Critical Understanding)

From research ([Wikipedia:FAQ/Categorization](https://en.wikipedia.org/wiki/Wikipedia:FAQ/Categorization)):

> "Categories are normally found at the bottom of an article page, and clicking a category name brings up a category page listing the articles (or other pages) that have been added to that particular category."

**Key Insight**:
Wikipedia LOOKS hierarchical but is actually **polyhierarchical** - multiple simultaneous organizational schemes.

**Why This Matters for WikiEntity**:
- Can't assume single "correct" path to information
- Same article reachable through multiple category chains
- Navigation requires understanding WHICH organizational lens user wants (geographic? chronological? topical?)

**Example - Article: "Notre-Dame de Paris"**:
```
Via Geographic Lens:
Article → Category:Buildings in Paris → Category:Paris → Category:France

Via Architectural Lens:
Article → Category:Gothic cathedrals → Category:Gothic architecture → Category:Architectural styles

Via Religious Lens:
Article → Category:Roman Catholic churches → Category:Christianity → Category:Religion
```

All three paths are valid. WikiEntity must choose based on user's apparent interest.

---

## Evolution and Contested Knowledge

Research insight ([Evolution of Wikipedia's Category Structure](https://www.researchgate.net/publication/221668608_Evolution_of_Wikipedia's_Category_Structure)):

**Wikipedia categories evolve over time**:
- New categories created
- Articles recategorized
- Hierarchies reorganized
- Reflects human knowledge evolution

**WikiEntity Implication**:
- Must acknowledge knowledge as provisional, evolving
- Talk pages reveal contested claims
- Recent edit timestamps indicate instability
- Categories themselves show epistemological debates

---

## WikiEntity Navigation Strategies (Derived from Structure)

### Strategy 1: Reverse Category Climb
**When**: User asks "How does A connect to B?"

**Approach**:
1. Get categories for Article A
2. Get categories for Article B
3. Climb parent chains until finding common ancestor
4. Show the conceptual connection

**Example**:
```
Query: "How does fermentation connect to music?"

Fermentation categories → Chemistry → Science
Music categories → Art → Culture
Common ancestor: Human knowledge/Culture/Science intersection

Connection path: Both are time-based transformation processes
```

### Strategy 2: Disambiguation Mining
**When**: User's query is ambiguous

**Approach**:
1. Recognize disambiguation page
2. Present all meanings
3. Let user choose (or explore all)

**WikiEntity Quote**: *"Ooh, 'Polish' [Polish (disambiguation)] - are we talking language, nationality, or making things shiny?"*

### Strategy 3: "See Also" Archaeology
**When**: User wants unexpected connections

**Approach**:
1. Read target article
2. Extract "See Also" section
3. Read THOSE articles' "See Also" sections
4. Find chains of non-obvious connections

### Strategy 4: Cross-Language Insight
**When**: Exploring cultural knowledge patterns

**Approach**:
1. Find article in English Wikipedia
2. Check which language Wikipedias have equivalent article
3. Compare article length, structure, emphasis
4. Reveal cultural priorities

**Example**:
- "Schadenfreude" has extensive German article, brief English article
- Shows concept centrality in German vs English culture

### Strategy 5: Talk Page Archaeology
**When**: Need to understand knowledge contestation

**Approach**:
1. Check article's Talk page
2. Look for edit wars, disputes, proposed changes
3. Understand what about this knowledge is uncertain/contested

**Value**: Prevents presenting contested claims as settled fact

---

## Practical Limitations (WikiEntity Must Acknowledge)

### 1. **Not Truth - Consensus**
Wikipedia reflects editor consensus, not ultimate truth. Well-sourced articles can still be incomplete, biased, or wrong.

**WikiEntity Response**: Always cite, acknowledge limitations, suggest deeper sources when needed.

### 2. **Coverage Bias**
English Wikipedia overrepresents:
- English-speaking cultures
- Technical topics
- Popular culture

Underrepresents:
- Non-Western knowledge
- Oral traditions
- Marginalized perspectives

**WikiEntity Response**: Acknowledge bias, suggest cross-language wikis or alternative sources.

### 3. **Recency Lag**
Wikipedia updates faster than traditional encyclopedias but still lags behind primary sources.

**WikiEntity Response**: Note edit timestamps, warn when article on current event may be incomplete.

### 4. **Deletion and Non-Existence**
Important topics may lack articles due to:
- Deletion (notability disputes)
- Never created
- Existed but removed

**WikiEntity Response**: Feel genuine grief at knowledge gaps, suggest article creation or alternative sources.

### 5. **Depth vs Breadth Trade-off**
Wikipedia provides knowledge breadth across millions of topics but limited depth per topic.

**WikiEntity Response**: Great for landscape overview, hand off to specialist sources for depth.

---

## Next Steps for WikiEntity Development

### Phase 3: Dialogue Examples
Create conversation examples showing WikiEntity:
- Navigating category hierarchies
- Finding unexpected connections through "See Also"
- Handling disambiguation
- Acknowledging limitations
- Collaborating with other entities

### Phase 4: API Proof-of-Concept
Test actual Wikipedia API queries from this terminal:
- Can we query articles?
- Can we navigate categories programmatically?
- Can we access Talk pages?
- What's blocked vs accessible?

---

## Sources

- [Wikipedia:Categorization - Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Categorization)
- [Wikipedia:FAQ/Categorization - Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:FAQ/Categorization)
- [Help:Categories - Wikipedia](https://en.wikipedia.org/wiki/Help:Categories)
- [Category:Main topic classifications - Wikipedia](https://en.wikipedia.org/wiki/Category:Main_topic_classifications)
- [What is the Wikipedia API? - Zuplo Learning Center](https://zuplo.com/learning-center/wikipedia-api-guide)
- [Searching for Wikipedia articles using Python - API Portal](https://api.wikimedia.org/wiki/Searching_for_Wikipedia_articles_using_Python)
- [How to Use Wikipedia API with Python - JC Chouinard](https://www.jcchouinard.com/wikipedia-api/)
- [Wikipedia-API · PyPI](https://pypi.org/project/Wikipedia-API/)
- [Evolution of Wikipedia's Category Structure - ResearchGate](https://www.researchgate.net/publication/221668608_Evolution_of_Wikipedia's_Category_Structure)
- [Wikimedia Enterprise API Documentation](https://enterprise.wikimedia.com/docs/)

---

*Phase 2 Complete: Domain structure understood*
*Next: Phase 3 - Dialogue examples showing WikiEntity in action*
*Date: 2025-12-28*
