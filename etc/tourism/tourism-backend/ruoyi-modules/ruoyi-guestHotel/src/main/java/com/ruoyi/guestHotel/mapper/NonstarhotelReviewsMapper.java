package com.ruoyi.guestHotel.mapper;

import com.ruoyi.guestHotel.domain.NonstarhotelReviews;

import java.util.List;

public interface NonstarhotelReviewsMapper {
    /**
     * 查询星级酒店评论列表
     *
     * @param id 星级酒店ID
     * @return 指定星级酒店房间集合
     */
    public List<NonstarhotelReviews> selectNonstarhotelReviewsList(Long id);
}
