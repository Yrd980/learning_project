package com.ruoyi.guestHotel.controller;

import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;

import com.ruoyi.guestHotel.domain.*;
import com.ruoyi.guestHotel.domain.VO.NonstarhotelReviewsVO;
import com.ruoyi.guestHotel.service.INonstarhotelRoomsService;
import com.ruoyi.guestHotel.service.INonstarhotelsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/guest/nonstarhotels")
public class NonstarhotelRoomsController extends BaseController {
    @Autowired
    private INonstarhotelRoomsService nonstarhotelRoomsService;
    @Autowired
    private INonstarhotelsService nonstarhotelsService;

    /**
     * 查询非星级酒店房间列表
     */

    @GetMapping("/details/{id}")
    public List<Object> list(@PathVariable("id") Long id)
    {
        startPage();
        List<Object> lst=new ArrayList<>();
        List<NonstarhotelRooms> list = nonstarhotelRoomsService.selectNonstarhotelRoomsList(id);
        Nonstarhotels sh= nonstarhotelsService.selectNonstarhotelsById(id);

        List<NonstarhotelReviews> list_reviews= nonstarhotelRoomsService.selectNonstarhotelReviewsList(id);
        List<NonstarhotelReviewsVO> reviewsVOList1=new ArrayList<>();
        list_reviews.forEach(review ->{
            NonstarhotelReviewsVO nonstarhotelReviewsVO=new NonstarhotelReviewsVO();
            nonstarhotelReviewsVO.setContent(review.getContent());
            String guestName=nonstarhotelRoomsService.selectUserInfoById(review.getGuest_id()).getUser_name();
            nonstarhotelReviewsVO.setGuest_name(guestName);
            nonstarhotelReviewsVO.setRating(review.getRating());
            nonstarhotelReviewsVO.setReview_date(review.getReview_date());
            String avatar=nonstarhotelRoomsService.selectUserInfoById(review.getGuest_id()).getAvatar();
            nonstarhotelReviewsVO.setAvatar(avatar);
            String roomName=nonstarhotelRoomsService.selectNonstarhotelRoomsById(review.getRoom_type_id()).getName();
            nonstarhotelReviewsVO.setRoom_type_name(roomName);
            reviewsVOList1.add(nonstarhotelReviewsVO);
        });
        lst.add(list);
        lst.add(sh);
        lst.add(reviewsVOList1);
        return lst;
    }
    /**
     * 新增非星级酒店预订信息
     */

    @PostMapping("/details/{id}")
    public AjaxResult add(@RequestBody NonstarBookings nonstarBookings)
    {
        return toAjax(nonstarhotelRoomsService.insertNonstarhotelBookingMsg(nonstarBookings));
    }
}
