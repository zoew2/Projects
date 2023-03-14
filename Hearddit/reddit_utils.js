const axios = require('axios');

let lastSubreddit = null;
let lastPostNumber = 0;
let lastPostID = 0;

class RedditUtils {

    static getPostNumber(subreddit, totalPosts) {
        if (lastSubreddit === subreddit) {
            lastPostNumber = (lastPostNumber + 1) % totalPosts;
        } else {
            lastPostNumber = 0;
            lastSubreddit = subreddit
        }
        return lastPostNumber;
    }

    async getPosts(subreddit, sortBy) {

        const sort = sortBy ? sortBy : 'top';
        const url = 'https://www.reddit.com/r/' + subreddit + '/' + sort + '.json';

        return await axios.get(url)
            .then(response => {
                const postNum = RedditUtils.getPostNumber(subreddit, response.data.data.children.length - 1);
                lastPostID = response.data.data.children[postNum].data.name;
                return response.data.data.children[postNum].data;
            }).catch(error => {
                return {error: "Error geting posts from " + subreddit + ":" + error}
            });
    }

    static async vote(direction, accessToken) {
        const url = 'https://oauth.reddit.com/api/vote';
        const headers = {Authorization: "Bearer " + accessToken};

        return await axios.post(url, {
            id: lastPostID,
            dir: direction.toString()
        }, {
            headers: headers
        }).then(response => {
            return response.data;
        }).catch(error => {
            return {error: "Error voting: " + error}
        })
    }
}

module.exports = RedditUtils;
